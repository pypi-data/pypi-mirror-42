# Copyright (c) 2018 Manfred Moitzi
# License: MIT License
from ezdxf.lldxf.const import DXFStructureError, DXFValueError
from ezdxf.lldxf.types import DXFTag
from ezdxf.algebra.matrix44 import Matrix44


def get_matrix(subclass, code):
    values = [tag.value for tag in subclass.find_all(code)]
    if len(values) != 16:
        raise DXFStructureError('Invalid transformation matrix.')
    return Matrix44(values)


def set_matrix(subclass, code, data):
    values = list(data)
    if len(values) != 16:
        raise DXFValueError("Transformation matrix requires 16 values.")

    try:
        insert_pos = subclass.tag_index(code)
    except DXFValueError:
        insert_pos = len(subclass)
    subclass.remove_tags((code,))
    tags = [DXFTag(code, value) for value in values]
    subclass[insert_pos:insert_pos] = tags
