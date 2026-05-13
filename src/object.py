from utils.api_tools import make_call
from shared import URL, OBJ


def unpack_object(object_obj: dict, sub_objects: bool = True):
    """Pulls out name, id, and properties for use"""
    object_dict = {
        "name": object_obj["name"],
        "id": object_obj["id"],
        "type": object_obj["type"]["name"],
    }
    for prop in object_obj["properties"]:
        prop_type = prop["format"]
        prop_value = None
        # Basic props that match their type
        if prop_type in ["checkbox", "date", "number", "text", "url"]:
            prop_value = prop[prop_type]

        elif prop_type in ["select", "multiselect"]:
            prop_value = prop[prop_type]["name"]

        elif prop_type == "objects" and sub_objects is True:
            continue
        object_dict[prop["name"]] = prop_value

    return object_dict


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
    object_url = URL + space_id + OBJ
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
