# Created: 25.03.2011
# Copyright (c) 2011-2018, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals

from ezdxf.lldxf.const import DXFInternalEzdxfError
from ezdxf.lldxf import const

from .graphics import GraphicEntity, ExtendedTags, make_attribs, DXFAttr

_DIMENSION_TPL = """0
DIMENSION
5
0
2
*BLOCKNAME
3
DIMSTYLE
10
0.0
20
0.0
30
0.0
11
0.0
21
0.0
31
0.0
12
0.0
22
0.0
32
0.0
70
0
1

13
0.0
23
0.0
33
0.0
14
0.0
24
0.0
34
0.0
15
0.0
25
0.0
35
0.0
16
0.0
26
0.0
36
0.0
40
1.0
50
0.0
"""


class Dimension(GraphicEntity):
    __slots__ = ()
    TEMPLATE = ExtendedTags.from_text(_DIMENSION_TPL)
    DXFATTRIBS = make_attribs({
        'geometry': DXFAttr(2),  # name of pseudo-Block containing the current dimension  entity geometry
        'dimstyle': DXFAttr(3, default='STANDARD'),  # dimension style name
        # The dimension style is stored in Drawing.sections.tables.dimstyles,
        # shortcut Drawings.dimstyles property
        'defpoint': DXFAttr(10, xtype='Point2D/3D'),  # WCS, definition point for all dimension types
        'text_midpoint': DXFAttr(11, xtype='Point2D/3D'),  # OCS, middle point of dimension text
        'translation_vector': DXFAttr(12, xtype='Point3D'),  # OCS, dimension block translation vector
        'dimtype': DXFAttr(70, default=0),  # Dimension type:
        # Values 0-6 are integer values that represent the dimension type.
        # Values 64 and 128 are bit values, which are added to the integer values
        # 0 = Rotated, horizontal, or vertical;
        # 1 = Aligned
        # 2 = Angular;
        # 3 = Diameter;
        # 4 = Radius
        # 5 = Angular 3 point;
        # 6 = Ordinate
        # 64 = Ordinate type. This is a bit value (bit 7) used only with integer
        # value 6. If set, ordinate is X-type; if not set, ordinate is Y-type
        # 128 = This is a bit value (bit 8) added to the other group 70 values if
        # the dimension text has been positioned at a user-defined location
        # rather than at the default location
        'user_text': DXFAttr(1),  # dimension text explicitly entered by the user.
        # If null or "<>", the dimension measurement is drawn as the text,
        # if " " [one blank space], the text is suppressed.
        # Anything else is drawn as the text.
        'defpoint2': DXFAttr(13, xtype='Point2D/3D'),  # WCS, definition point for linear and angular dimensions
        'defpoint3': DXFAttr(14, xtype='Point2D/3D'),  # WCS, definition point for linear and angular dimensions
        'defpoint4': DXFAttr(15, xtype='Point2D/3D'),  # WCS, definition point for diameter, radius, and angular dimensions
        'defpoint5': DXFAttr(16, xtype='Point2D/3D'),  # OCS, point defining dimension arc for angular dimensions
        'leader_length': DXFAttr(40),  # leader length for radius and diameter dimensions
        'angle': DXFAttr(50),  # angle of rotated, horizontal, or vertical linear dimensions
        'horizontal_direction': DXFAttr(51),
        # In addition, all dimension types have an optional group
        # (code 51) that indicates the horizontal direction for the
        # Dimension entity. This determines the orientation of
        # dimension text and dimension lines for horizontal,
        # vertical, and rotated linear dimensions. The group value
        # is the negative of the Entity Coordinate Systems (ECS)
        # angle of the UCS X axis in effect when the Dimension was
        # drawn. The X axis of the UCS in effect when the Dimension
        # was drawn is always parallel to the XY plane for the
        # Dimension's ECS, and the angle between the UCS X axis and
        # the ECS X axis is a single 2D angle. The value in group 51
        # is the angle from horizontal (the effective X axis) to the
        # ECS X axis. Entity Coordinate Systems (ECS) are described
        # later in this section.
        'oblique_angle': DXFAttr(52),
        # Linear dimension types with an oblique angle have an
        # optional group (code 52).When added to the rotation angle
        # of the linear dimension (group code 50) this gives the
        # angle of the extension lines
        'dim_text_rotation': DXFAttr(53),
        # The optional group code 53  is the rotation angle of the
        # dimension text away from its default orientation (the direction
        # of the dimension line).
    })

    @property
    def dim_type(self):
        return self.dxf.dimtype & 7

    @property
    def dim_type_name(self):
        return const.DimensionTypeNames[self.dim_type]

    def dim_style(self):
        if self.drawing is not None:
            dim_style_name = self.dxf.dimstyle
            # raises ValueError if not exists, but all used dim styles should exists!
            return self.drawing.dimstyles.get(dim_style_name)
        else:
            raise DXFInternalEzdxfError('Dimension.drawing attribute not initialized.')
