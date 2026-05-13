from utils.api_tools import make_call
from utils.unpacker import unpack_object
from shared import URL, OBJ


def get_object_by_id(space_id: str, object_id: str, simple: bool = True):
    """Pulls detailed object data by id"""
    object_url = URL + space_id
    object_url += OBJ + object_id

    object_obj = make_call("get", object_url, "get object by id")["object"]

    if object_obj is None:
        return "raise exception"

    object_formatted = None

    if isinstance(object_obj, str):
        return {"Clear me": object_obj["id"]}

    if simple:
        object_formatted = unpack_object(object_obj, False)
        return object_formatted

    return object_obj


def update_object(space_id, object_name: str, object_id: str, data: dict):
    """Updates object with provided data"""
    object_url = URL + space_id
    object_url += OBJ + object_id
    return make_call("patch", object_url, f"update object ({object_name}) by id", data)


def create_object(space_id: str, data: dict):
    """Creates object with provided data"""
    object_url = URL + space_id
    object_url += "/objects"
    return make_call(
        "post",
        object_url,
        f"create object {data['name']} with {data['type_key']} data",
        data,
    )


def delete_object(space_id, object_name: str, object_id: str):
    """Deletes object by id"""
    object_url = URL + space_id
    object_url += OBJ + object_id
    return make_call(
        "delete",
        object_url,
        f"delete object ({object_name}) by id",
    )
