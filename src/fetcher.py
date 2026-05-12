from utils.logger import logger
from utils.unpacker import unpack_object
from utils.api_tools import make_call
from shared import URL, OBJ, PROPS


class Fetcher:
    def search(self, space_id, search_name, search_body: dict, simple: bool = True):
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

    def get_types(self, space_id, system_types=None, props: bool = False):
        types_url = URL + space_id
        types_url += "/types"

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
            type_templates = self.get_templates(space_id, type_dict["id"])
            if type_templates is not None:
                type_dict["templates"] = {}
            for template in type_templates["data"]:
                type_dict["templates"][template["name"]] = template["id"]
            types_formatted[type_obj["name"]] = type_dict

        return types_formatted

    def get_templates(
        self,
        space_id,
        type_id,
    ):
        templates_url = URL + space_id
        templates_url += "/types/" + type_id
        templates_url += "/templates"

        templates = make_call("get", templates_url, "get templates from type")

        return templates

    def get_lists(self, space_id, query_type_id):
        list_ids = self.search(space_id, "collect queries", {"types": [query_type_id]})

        query_dict = {}
        for list_id in list_ids:
            query_dict[list_id] = {"id": list_ids[list_id]}
            view_list = self.get_views_list(space_id, list_ids[list_id])
            for view in view_list:
                query_dict[list_id][view["name"]] = view["id"]
        return query_dict

    def get_views_list(
        self,
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
        self,
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
                objs_to_check.append(self.get_object_by_id(space_id, obj["id"]))

        return objs_to_check

    def get_object_by_id(self, space_id: str, object_id: str, simple: bool = True):
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

    def get_property_list(self, space_id, system_props=None):
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
                    formatted_props[prop["name"]]["options"] = self.get_tags_from_prop(
                        space_id, prop["id"]
                    )
            return formatted_props
        return {}

    def get_tags_from_prop(self, space_id: str, prop_id: str):
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
