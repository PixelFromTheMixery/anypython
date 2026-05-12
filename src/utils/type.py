from utils.api_tools import make_call
from shared import URL


class Object:
    def create_type(self, space_id, type_data: dict):
        """Creates a type with the provided data"""
        type_url = URL + space_id
        type_url += "/types"
        type_dict = type_data.copy()
        del type_dict["id"]

        make_call("post", type_url, f"create type {type_dict['name']}", type_dict)

    def delete_type(self, space_id, type_data: dict):
        """Creates a type with the provided data"""
        type_url = URL + space_id
        type_url += "/types/" + type_data["id"]

        make_call("delete", type_url, f"delete type {type_data['key']}")

    def update_type(self, space_id: str, type_id: str, type_name: str, type_data: dict):
        """Patches a type with the provided data"""
        type_url = URL + space_id
        type_url += "/types/" + type_id

        make_call("patch", type_url, f"update type {type_name}", type_data)
