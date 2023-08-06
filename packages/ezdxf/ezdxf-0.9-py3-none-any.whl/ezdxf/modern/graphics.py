# Created: 25.03.2011
# Copyright (c) 2011-2018, Manfred Moitzi
# License: MIT License
from typing import TYPE_CHECKING, Tuple
from ezdxf.legacy import graphics as r12graphics
from ezdxf.lldxf.extendedtags import ExtendedTags
from ezdxf.lldxf.attributes import DXFAttr, DXFAttributes, DefSubclass, XType
from ezdxf.tools.rgb import int2rgb, rgb2int
from ezdxf.tools import float2transparency, transparency2float

if TYPE_CHECKING:
    from ezdxf.eztypes import Auditor

none_subclass = DefSubclass(None, {
    'handle': DXFAttr(5),
    'owner': DXFAttr(330),  # Soft-pointer ID/handle to owner BLOCK_RECORD object
})

entity_subclass = DefSubclass('AcDbEntity', {
    'paperspace': DXFAttr(67, default=0),  # 0 .. modelspace, 1 .. paperspace
    'layer': DXFAttr(8, default='0'),  # layername as string
    'linetype': DXFAttr(6, default='BYLAYER'),  # linetype as string, special names BYLAYER/BYBLOCK
    'lineweight': DXFAttr(370),  # Stored and moved around as a 16-bit integer
    # Line weight in mm times 100 (e.g. 0.13mm = 13). Smallest line weight is 13 and biggest line weight is 200, values
    # outside this range prevents AutoCAD from loading the file.
    # Special values:
    # LINEWEIGHT_BYLAYER = -1
    # LINEWEIGHT_BYBLOCK = -2
    # LINEWEIGHT_DEFAULT = -3
    'ltscale': DXFAttr(48, default=1.0),  # linetype scale
    'invisible': DXFAttr(60, default=0),  # invisible .. 1, visible .. 0
    'color': DXFAttr(62, default=256),  # dxf color index, 0 .. BYBLOCK, 256 .. BYLAYER
    'true_color': DXFAttr(420, dxfversion='AC1018'),  # true color as 0x00RRGGBB 24-bit value
    'color_name': DXFAttr(430, dxfversion='AC1018'),  # color name as string
    'transparency': DXFAttr(440, dxfversion='AC1018'),  # transparency value 0x020000TT 0 = fully transparent / 255 = opaque
    'shadow_mode': DXFAttr(284, dxfversion='AC1021'),  # shadow_mode
    # 0 = Casts and receives shadows
    # 1 = Casts shadows
    # 2 = Receives shadows
    # 3 = Ignores shadows

})


# noinspection PyUnresolvedReferences
class ModernGraphicEntityExtension:
    __slots__ = ()

    @property
    def rgb(self) -> Tuple[int, int, int]:
        return int2rgb(self.get_dxf_attrib('true_color'))

    @rgb.setter  # line.rgb = (12, 34, 56)
    def rgb(self, rgb: Tuple[int, int, int])->None:
        self.set_dxf_attrib('true_color', rgb2int(rgb))

    @property
    def transparency(self) -> float:
        return transparency2float(self.get_dxf_attrib('transparency'))

    @transparency.setter  # line.transparency = 0.50
    def transparency(self, transparency: float) -> None:
        # 0.0 = opaque & 1.0 if 100% transparent
        self.set_dxf_attrib('transparency', float2transparency(transparency))


class ModernGraphicEntity(r12graphics.GraphicEntity, ModernGraphicEntityExtension):
    __slots__ = ()
    """
    Default graphic entity wrapper, allows access to following dxf attributes:

        - handle
        - owner handle
        - layer
        - linetype
        - lineweight
        - color
        - paperspace
        - ltscale
        - invisible
        - true_color (as int), requires DXF Version AC1018 (AutoCAD R2004)
        - color_name, requires DXF Version AC1018 (AutoCAD R2004)
        - transparency, requires DXF Version AC1018 (AutoCAD R2004)
        - shadow_mode, requires DXF Version AC1021 (AutoCAD R2007)

    Wrapper for all unsupported graphic entities.

    """
    DXFATTRIBS = DXFAttributes(none_subclass, entity_subclass)

    def audit(self, auditor: 'Auditor') -> None:
        super(ModernGraphicEntity, self).audit(auditor)
        auditor.check_pointer_target_exists(self, zero_pointer_valid=False)


_LINETEMPLATE = """0
LINE
5
0
330
0
100
AcDbEntity
8
0
100
AcDbLine
10
0.0
20
0.0
30
0.0
11
1.0
21
1.0
31
1.0
"""

line_subclass = DefSubclass('AcDbLine', {
    'start': DXFAttr(10, xtype=XType.any_point),
    'end': DXFAttr(11, xtype=XType.any_point),
    'thickness': DXFAttr(39, default=0),
    'extrusion': DXFAttr(210, xtype=XType.point3d, default=(0.0, 0.0, 1.0)),
})


class Line(r12graphics.Line, ModernGraphicEntityExtension):
    __slots__ = ()
    TEMPLATE = ExtendedTags.from_text(_LINETEMPLATE)
    DXFATTRIBS = DXFAttributes(none_subclass, entity_subclass, line_subclass)


_POINT_TPL = """0
POINT
5
0
330
0
100
AcDbEntity
8
0
100
AcDbPoint
10
0.0
20
0.0
30
0.0
"""
point_subclass = DefSubclass('AcDbPoint', {
    'location': DXFAttr(10, xtype=XType.any_point),
    'thickness': DXFAttr(39, default=None),
    'extrusion': DXFAttr(210, xtype=XType.point3d, default=(0.0, 0.0, 1.0)),
})


class Point(r12graphics.Point, ModernGraphicEntityExtension):
    __slots__ = ()
    TEMPLATE = ExtendedTags.from_text(_POINT_TPL)
    DXFATTRIBS = DXFAttributes(none_subclass, entity_subclass, point_subclass)


_CIRCLE_TPL = """0
CIRCLE
5
0
330
0
100
AcDbEntity
8
0
100
AcDbCircle
10
0.0
20
0.0
30
0.0
40
1.0
"""
circle_subclass = DefSubclass('AcDbCircle', {
    'center': DXFAttr(10, xtype=XType.any_point),
    'radius': DXFAttr(40),
    'thickness': DXFAttr(39, default=0.0),
    'extrusion': DXFAttr(210, xtype=XType.point3d, default=(0.0, 0.0, 1.0)),
})


class Circle(r12graphics.Circle, ModernGraphicEntityExtension):
    __slots__ = ()
    TEMPLATE = ExtendedTags.from_text(_CIRCLE_TPL)
    DXFATTRIBS = DXFAttributes(none_subclass, entity_subclass, circle_subclass)


_ARC_TPL = """0
ARC
5
0
330
0
100
AcDbEntity
8
0
100
AcDbCircle
10
0.0
20
0.0
30
0.0
40
1.0
100
AcDbArc
50
0
51
360
"""

arc_subclass = DefSubclass('AcDbArc', {
    'start_angle': DXFAttr(50),
    'end_angle': DXFAttr(51),
})


class Arc(r12graphics.Arc, ModernGraphicEntityExtension):
    __slots__ = ()
    TEMPLATE = ExtendedTags.from_text(_ARC_TPL)
    DXFATTRIBS = DXFAttributes(none_subclass, entity_subclass, circle_subclass, arc_subclass)


class SeqEnd(r12graphics.SeqEnd):
    __slots__ = ()
    TEMPLATE = ExtendedTags.from_text("  0\nSEQEND\n  5\n0\n330\n 0\n100\nAcDbEntity\n")
    DXFATTRIBS = DXFAttributes(none_subclass, entity_subclass)


_SHAPE_TPL = """0
SHAPE
5
0
330
0
100
AcDbEntity
8
0
100
AcDbShape
10
0.0
20
0.0
30
0.0
40
1.0
2
NAME
50
0.0
41
1.0
51
0.0
"""

shape_subclass = DefSubclass('AcDbShape', {
    'thickness': DXFAttr(39, default=0.0),
    'insert': DXFAttr(10, xtype=XType.any_point),
    'size': DXFAttr(40),
    'name': DXFAttr(2),
    'rotation': DXFAttr(50, default=0.0),
    'xscale': DXFAttr(41, default=1.0),
    'oblique': DXFAttr(51, default=0.0),
    'extrusion': DXFAttr(210, xtype=XType.point3d, default=(0.0, 0.0, 1.0)),
})


# SHAPE is not tested with real world DXF drawings!
class Shape(ModernGraphicEntity):
    __slots__ = ()
    TEMPLATE = ExtendedTags.from_text(_SHAPE_TPL)
    DXFATTRIBS = DXFAttributes(none_subclass, entity_subclass, shape_subclass)
