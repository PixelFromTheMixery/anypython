# region Docs
"""
Pydantic classes to make Anytype entity shapes

Regular data classes were considered,
but Anytype uses pydantic for their REST API anyway

All id's are optional to allow for creation of entities

Classes:
    All classes assumed to have a BaseModel Parent

    AnytypeBasic: Just name and ID, used for processing from lists
    AnytypeOption: Option on select or multi-select property
    AnytypeProp: A data field on an object
    AnytypeType: Object classification
    AnytypeObject: Essentially a pretty markdown
    AnytypeList: A realtime collection of objects
"""
# endregion

from typing import Optional

from pydantic import BaseModel


class AnyTypeBasic(BaseModel):
    # region Docs
    """
    Just name and ID, used for processing from lists

    Attributes:
        id (str): entity id
        name (str): pretty name
    """

    # endregion

    id: str
    name: str


class AnytypeOption(BaseModel):
    # region Docs
    """
    Option on select or multi-select property

    Attributes:
        id (str): entity id
        key (str): unique option identifier
        name (str): pretty name
        color (str): option color
    """

    # endregion

    id: Optional[str] = None
    key: str
    name: str
    color: str


class AnytypeProp(BaseModel):
    # region Docs
    """
    AnytypeProp: A data field on an object

    Attributes:
        id (str): entity id
        key (str): unique option identifier
        name (str): pretty name
        format (str): type of prop, number, date, etc.
        options (str): option field for select and multi-select property
    """

    # endregion

    id: Optional[str] = None
    key: str
    name: str
    format: str
    options: Optional[list[AnytypeOption]] = None


class AntypeType(BaseModel):
    # region Docs
    """
    Object classification

    Attributes:
        id (str): entity id
        key (str): unique option identifier
        name (str): pretty name
        plural_name (str): display for collections
        layout (str): object shape
        icon (str): simple shape to represent object shape
        properties (AnytypeProps): properties of type

    """

    # endregion

    id: Optional[str] = None
    name: str
    key: str
    plural_name: str
    layout: str
    icon: str
    properties: list[AnytypeProp]


class AnytypeObject(BaseModel):
    # region Docs
    """
    Essentially a pretty markdown

    Attributes:
        id (str): entity id
        name (str): pretty name
        type (str): object type
        properties (lost[AnytypeProp]): object properties, doesn't have to match type
        markdown (str): Optional, page contents

    """

    # endregion

    id: Optional[str] = None
    name: str
    type: str
    properties: list[AnytypeProp]
    markdown: Optional[str] = None


class AnytypeList(BaseModel):
    # region Docs
    """
    A realtime collection of objects

    Attributes:
        id (str): entity id
        name (str): pretty name
        views (AnytypeBasic): filtered perspectives
    """

    # endregion

    id: str
    name: str
    views: list[AnyTypeBasic]
