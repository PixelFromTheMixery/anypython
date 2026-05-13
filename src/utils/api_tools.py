# region Docs
"""
API tool for interacting with an anytype instance.

Performs the actual API calls if API key and url is supplied, optional data

Variables:
    # Call-based
    RETRIES (int): Number of request retries
    DELAY (int): Number of seconds between between retries
    TIMEOUT (int): How long to wait for a hang

    RESPONSE_MAP (dict): lambda map of API request types

    HEADERS (dict): sets up anytype api response for reuse

Methods:
    make_call: Performs the actual contact with Anytype
"""
# endregion

import random
import time

import requests

from settings import fetch_settings
from logger import logger

RETRIES: int = 3
DELAY: int = 2
TIMEOUT: int = 3

RESPONSE_MAP = {
    "delete": lambda u, h: requests.delete(u, headers=h, timeout=TIMEOUT),
    "get": lambda u, h: requests.get(u, headers=h, timeout=TIMEOUT),
    "patch": lambda u, h, d: requests.patch(
        u,
        headers=h,
        timeout=TIMEOUT,
        json=d if isinstance(d, dict) else None,
        data=d if isinstance(d, str) else None,
    ),
    "post": lambda u, h, d: requests.post(
        u,
        headers=h,
        timeout=TIMEOUT,
        json=d if isinstance(d, dict) else None,
        data=d if isinstance(d, str) else None,
    ),
    "put": lambda u, h, d: requests.put(
        u,
        headers=h,
        timeout=TIMEOUT,
        json=d if isinstance(d, dict) else None,
        data=d if isinstance(d, str) else None,
    ),
}

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + fetch_settings().anypython_key,
    "Anytype-Version": "2025-11-08",
}


def make_call(
    category: str,
    url: str,
    info: str,
    data: dict = None,
):
    # region Docs
    """
    Makes a call based on method, url, and info

    Args:
        category (str): REST method
        url (str): url to make call to
        info (str): string for logging to explain what the call is doing
        data (dict): mapping of call values

    Returns:
        dict: json value of api response.

    Raises:
        ConnectionError/Timeout: Infinite attempts until able to contact instance.
        HTTPError(429): Too many calls, gives some time to wait until next delay
        Other: Any other issue, possibly from Anytype
    """
    # endregion

    attempt = 0
    while True:
        try:
            logger.info("Attempt to %s: %s of %s", info, attempt, RETRIES)

            response = (
                RESPONSE_MAP[category](url, HEADERS, data)
                if category in ["patch", "post", "put"]
                else RESPONSE_MAP[category](url, HEADERS)
            )

            response.raise_for_status()
            return response.json()

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            wait_time = 60 + random.uniform(0, 5)
            logger.warning(
                "Network issue (%s). Retrying infinitely... Next try in %.1f",
                e,
                wait_time,
            )
            time.sleep(wait_time)
            continue  # Restarts the 'while True' loop immediately

        except requests.exceptions.HTTPError as e:
            if response.status_code == 429 and attempt <= RETRIES - 1:
                attempt += 1
                logger.warning(
                    "429 limit hit. Retry %s/%s in %s...", attempt, RETRIES, DELAY
                )
                time.sleep(DELAY)
                continue

            # If it's not a 429, or we ran out of 429 retries, handle normally
            logger.error("RequestException: %s", {e})
            if attempt > RETRIES:
                raise
