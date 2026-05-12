from utils.api_tools import make_call
from shared import URL, OBJ


class Object:
    def update_object(self, space_id, object_name: str, object_id: str, data: dict):
        """Updates object with provided data"""
        object_url = URL + space_id
        object_url += OBJ + object_id
        return make_call(
            "patch", object_url, f"update object ({object_name}) by id", data
        )

    def create_object(self, space_id: str, data: dict):
        """Creates object with provided data"""
        object_url = URL + space_id
        object_url += "/objects"
        return make_call(
            "post",
            object_url,
            f"create object {data['name']} with {data['type_key']} data",
            data,
        )

    def delete_object(self, space_id, object_name: str, object_id: str):
        """Deletes object by id"""
        object_url = URL + space_id
        object_url += OBJ + object_id
        return make_call(
            "delete",
            object_url,
            f"delete object ({object_name}) by id",
        )
