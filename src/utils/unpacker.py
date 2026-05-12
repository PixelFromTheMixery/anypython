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
