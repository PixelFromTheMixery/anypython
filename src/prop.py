from utils.api_tools import make_call
from utils.models import AnytypeOption, AnytypeProp
from shared import URL, PROPS


def get_tags_from_prop(space_id: str, prop_id: str):
    """Returns the tag and name from the provided list"""
    tag_url = URL + space_id
    tag_url += PROPS + prop_id
    tag_url += "/tags"
    tags = make_call("get", tag_url, "get tags from property")
    formatted_tags = {}
    if tags["data"]:
        for tag in tags["data"]:
            formatted_tags[tag["name"]] = {
                "id": tag["id"],
                "key": tag["key"],
                "name": tag["name"],
                "color": tag["color"],
            }
        return formatted_tags
    return {}


def get_property_list(space_id, system_props=None):
    """Returns a list of all the properties of a space and their properties"""
    prop_url = URL + space_id
    prop_url += PROPS
    props = make_call("get", prop_url, f"get props from space {space_id}")
    system_props = [] if system_props is None else system_props
    formatted_props = {}
    if props["data"]:
        for prop in props["data"]:
            if prop["name"] in system_props:
                continue
            formatted_props[prop["name"]] = {
                "id": prop["id"],
                "key": prop["key"],
                "name": prop["name"],
                "format": prop["format"],
            }
            if prop["format"] in ["select", "multiselect"]:
                formatted_props[prop["name"]]["options"] = get_tags_from_prop(
                    space_id, prop["id"]
                )
        return formatted_props
    return {}


def add_option_to_property(
    space_id: str, prop: AnytypeProp, option: AnytypeOption
) -> AnytypeOption:
    """Adds option to provided property"""
    prop_url = URL + space_id
    prop_url += PROPS + prop.id
    prop_url += "/tags"
    new_tag_data = make_call(
        "post",
        prop_url,
        f"add {option.name} to property",
        option.model_dump(),
    )["tag"]

    new_tag = AnytypeOption(
        id=new_tag_data["id"],
        key=new_tag_data["key"],
        name=new_tag_data["name"],
        color=new_tag_data["data"],
    )

    return new_tag


def create_property(space_id: str, prop: AnytypeProp) -> str | None:
    """Adds property to space"""
    prop_url = URL + space_id
    prop_url += "/properties"

    new_prop = make_call(
        "post", prop_url, f"add property '{prop.name}' to space", prop.model_dump()
    )
    return new_prop["property"]["id"] if new_prop is not None else None


def delete_property(space_id, prop: AnytypeProp) -> None:
    """Removes property from space"""
    prop_url = URL + space_id
    prop_url += "/properties/" + prop.id
    prop_url = make_call("delete", prop_url, f"delete property {prop.name}")
