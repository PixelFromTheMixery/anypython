from utils.api_tools import make_call
from shared import URL, PROPS


class Prop:
    def add_tag_to_select_property(self, space_id: str, prop_id: str, data: dict):
        """Adds option to provided property"""
        prop_url = URL + space_id
        prop_url += PROPS + prop_id
        prop_url += "/tags"
        new_tag = make_call(
            "post",
            prop_url,
            f"add {data['name']} to property",
            data,
        )
        formatted_tag = {}
        if new_tag["tag"]:
            formatted_tag[new_tag["tag"]["name"]] = {
                "id": new_tag["tag"]["id"],
                "key": new_tag["tag"]["key"],
                "name": new_tag["tag"]["name"],
                "color": new_tag["tag"]["color"],
            }
        return formatted_tag

    def create_property(self, space_id: str, data: dict):
        """Adds property to space"""
        prop_url = URL + space_id
        prop_url += "/properties"
        prop_data = {
            "format": data["format"],
            "key": data["key"],
            "name": data["name"],
        }
        new_prop = make_call(
            "post", prop_url, f"add property '{data['name']}' to space", prop_data
        )
        return new_prop["property"]["id"] if new_prop is not None else None

    def delete_property(self, space_id, prop_dict):
        """Removes property from space"""
        prop_url = URL + space_id
        prop_url += "/properties/" + prop_dict["id"]
        prop_url = make_call("delete", prop_url, f"delete property {prop_dict['name']}")
