from utils.logger import logger
from utils.api_tools import make_call
from object import get_object_by_id, unpack_object
from shared import URL


def search(space_id, search_name, search_body: dict, simple: bool = True):
    """Returns all objects by type"""
    url = URL + space_id
    url += "/search?limit=999"
    objects = make_call("post", url, f"searching for {search_name}", search_body)

    if objects is not None and objects["data"] is None:
        return "No objects found"

    formatted_objects = {}
    for obj in objects["data"] if objects is not None else []:
        if simple:
            formatted_objects[obj["name"]] = obj["id"]
        else:
            formatted_objects[obj["name"]] = unpack_object(obj, False)

    return formatted_objects


def get_lists(space_id, query_type_id):
    list_ids = search(space_id, "collect queries", {"types": [query_type_id]})

    query_dict = {}
    for list_id in list_ids:
        query_dict[list_id] = {"id": list_ids[list_id]}
        view_list = get_views_list(space_id, list_ids[list_id])
        for view in view_list:
            query_dict[list_id][view["name"]] = view["id"]
    return query_dict


def get_views_list(
    space_id: str,
    list_id: str,
):
    """Pull all views in a query object"""
    views_url = URL + space_id
    views_url += "/lists/" + list_id
    views_url += "/views"

    views = make_call("get", views_url, "get view list for query")
    views_formatted = []

    for view in views["data"] if views is not None else []:
        views_formatted.append({"name": view["name"], "id": view["id"]})

    return views_formatted


def get_list_view_objects(
    space_id: str,
    list_id: str,
    view_id: str,
):
    """Pulls out detailed information of objects in a view (query)"""
    obj_url = URL + space_id
    obj_url += "/lists/" + list_id
    obj_url += "/views/" + view_id
    obj_url += "/objects"
    main_obj = make_call("get", obj_url, "get obj")

    objs_to_check = []

    if main_obj and "data" in main_obj:
        logger.info("Found %d objects", len(main_obj["data"]))

        for obj in main_obj["data"]:
            objs_to_check.append(get_object_by_id(space_id, obj["id"]))

    return objs_to_check
