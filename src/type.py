from utils.api_tools import make_call
from utils.models import AntypeType
from shared import URL

TYPES = "/types/"


def get_templates(
    space_id,
    type_id,
):
    templates_url = URL + space_id + TYPES + type_id
    templates_url += "/templates"

    templates = make_call("get", templates_url, "get templates from type")

    return templates


def get_types(space_id, system_types=None, props: bool = False):
    types_url = URL + space_id + TYPES

    types = make_call("get", types_url, "get types from space")
    types_formatted = {}

    system_types = [] if system_types is None else system_types
    for type_obj in types["data"] if types is not None else []:
        if type_obj["name"] in system_types:
            continue
        type_dict = {"id": type_obj["id"], "key": type_obj["key"]}
        if props:
            type_dict["plural_name"] = type_obj["plural_name"]
            type_dict["layout"] = type_obj["layout"]
            type_dict["name"] = type_obj["name"]
            type_dict["icon"] = type_obj["icon"]
            type_dict["properties"] = []
            for prop in type_obj["properties"]:
                type_dict["properties"].append(
                    {
                        "key": prop["key"],
                        "name": prop["name"],
                        "format": prop["format"],
                    }
                )
        type_templates = get_templates(space_id, type_dict["id"])
        if type_templates is not None:
            type_dict["templates"] = {}
        for template in type_templates["data"]:
            type_dict["templates"][template["name"]] = template["id"]
        types_formatted[type_obj["name"]] = type_dict

    return types_formatted


def create_type(space_id, atype: AntypeType) -> str | None:
    """Creates a type with the provided data"""
    type_url = URL + space_id + TYPES

    new_type = make_call(
        "post", type_url, f"create type {atype.name}", atype.model_dump
    )
    return new_type["object"]["id"] if new_type is not None else None


def delete_type(space_id, atype: AntypeType):
    """Creates a type with the provided data"""
    type_url = URL + space_id + TYPES + atype.id

    make_call("delete", type_url, f"delete type {atype.key}")


def update_type(space_id: str, atype: AntypeType):
    """Patches a type with the provided data"""
    type_url = URL + space_id + TYPES + atype.id

    make_call("patch", type_url, f"update type {atype.name}", atype.model_dump())
