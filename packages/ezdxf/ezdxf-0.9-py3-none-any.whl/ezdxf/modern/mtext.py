# Created: 24.05.2015
# Copyright (c) 2015-2018, Manfred Moitzi
# License: MIT License
from typing import TYPE_CHECKING, List, Union, Tuple
from contextlib import contextmanager
import math

from ezdxf.math.vector import Vector
from ezdxf.lldxf.attributes import DXFAttr, DXFAttributes, DefSubclass, XType
from ezdxf.lldxf.tags import DXFTag
from ezdxf.lldxf.extendedtags import ExtendedTags
from ezdxf.lldxf import const
from ezdxf.lldxf.const import DXFValueError
from ezdxf import rgb2int
from .graphics import none_subclass, entity_subclass, ModernGraphicEntity

if TYPE_CHECKING:
    from ezdxf.eztypes import Vertex

_MTEXT_TPL = """0
MTEXT
5
0
330
0
100
AcDbEntity
8
0
100
AcDbMText
40
1.0
71
1
73
1
1

"""

mtext_subclass = DefSubclass('AcDbMText', {
    'insert': DXFAttr(10, xtype=XType.point3d),
    'char_height': DXFAttr(40),  # nominal (initial) text height
    'width': DXFAttr(41),  # reference column width
    'attachment_point': DXFAttr(71),
    # 1 = Top left; 2 = Top center; 3 = Top right
    # 4 = Middle left; 5 = Middle center; 6 = Middle right
    # 7 = Bottom left; 8 = Bottom center; 9 = Bottom right
    'flow_direction': DXFAttr(72),
    # 1 = Left to right
    # 3 = Top to bottom
    # 5 = By style (the flow direction is inherited from the associated text style)
    'style': DXFAttr(7, default='STANDARD'),  # text style name
    'extrusion': DXFAttr(210, xtype=XType.point3d, default=(0.0, 0.0, 1.0)),
    'text_direction': DXFAttr(11, xtype=XType.point3d),  # x-axis direction vector (in WCS)
    # If *rotation* and *text_direction* are present, *text_direction* wins
    'rect_width': DXFAttr(42),  # Horizontal width of the characters that make up the mtext entity.
    # This value will always be equal to or less than the value of *width*, (read-only, ignored if supplied)
    'rect_height': DXFAttr(43),  # vertical height of the mtext entity (read-only, ignored if supplied)
    'rotation': DXFAttr(50, default=0.0),  # in degrees (circle=360 deg) -  error in DXF reference, which says radians
    'line_spacing_style': DXFAttr(73),  # line spacing style (optional):
    # 1 = At least (taller characters will override)
    # 2 = Exact (taller characters will not override)
    'line_spacing_factor': DXFAttr(44),  # line spacing factor (optional):
    # Percentage of default (3-on-5) line spacing to be applied. Valid values
    # range from 0.25 to 4.00
    'box_fill_scale': DXFAttr(45, dxfversion='AC1021'),
    # Determines how much border there is around the text.
    # (45) + (90) + (63) all three required, if one of them is used
    'bg_fill': DXFAttr(90, dxfversion='AC1021'),  # background fill type:
    # 0=off;
    # 1=color -> (63) < (421) or (431);
    # 2=drawing window color
    # 3=use background color
    'bg_fill_color': DXFAttr(63, dxfversion='AC1021'),  # background fill color as ACI, required even true color is used
    'bg_fill_true_color': DXFAttr(421, dxfversion='AC1021'),  # background fill color as true color value, (63) also required but ignored
    'bg_fill_color_name': DXFAttr(431, dxfversion='AC1021'),  # background fill color as color name ???, (63) also required but ignored
    'bg_fill_transparency': DXFAttr(441, dxfversion='AC1021'),  # background fill color transparency - not used by AutoCAD/BricsCAD

})


class MText(ModernGraphicEntity):  # MTEXT will be extended in DXF version AC1021 (ACAD 2007)
    __slots__ = ()
    TEMPLATE = ExtendedTags.from_text(_MTEXT_TPL)
    DXFATTRIBS = DXFAttributes(none_subclass, entity_subclass, mtext_subclass)

    def get_text(self) -> str:
        tags = self.tags.get_subclass('AcDbMText')
        tail = ""
        parts = []
        for tag in tags:
            if tag.code == 1:
                tail = tag.value
            if tag.code == 3:
                parts.append(tag.value)
        parts.append(tail)
        return "".join(parts)

    def set_text(self, text: str) -> 'MText':
        tags = self.tags.get_subclass('AcDbMText')
        tags.remove_tags(codes=(1, 3))
        str_chunks = split_string_in_chunks(text, size=250)
        if len(str_chunks) == 0:
            str_chunks.append("")
        while len(str_chunks) > 1:
            tags.append(DXFTag(3, str_chunks.pop(0)))
        tags.append(DXFTag(1, str_chunks[0]))
        return self

    def get_rotation(self) -> float:
        try:
            vector = self.dxf.text_direction
        except DXFValueError:
            rotation = self.get_dxf_attrib('rotation', 0.0)
        else:
            radians = math.atan2(vector[1], vector[0])  # ignores z-axis
            rotation = math.degrees(radians)
        return rotation

    def set_rotation(self, angle: float) -> 'MText':
        del self.dxf.text_direction  # *text_direction* has higher priority than *rotation*, therefore delete it
        self.dxf.rotation = angle
        return self

    def set_location(self, insert: 'Vertex', rotation: float = None, attachment_point: int = None) -> 'MText':
        self.dxf.insert = Vector(insert)
        if rotation is not None:
            self.set_rotation(rotation)
        if attachment_point is not None:
            self.dxf.attachment_point = attachment_point
        return self

    def set_bg_color(self, color: Union[int, str, Tuple[int, int, int], None], scale: float = 1.5):
        self.dxf.box_fill_scale = scale
        if color is None:
            self.del_dxf_attrib('bg_fill')
            self.del_dxf_attrib('box_fill_scale')
            self.del_dxf_attrib('bg_fill_color')
            self.del_dxf_attrib('bg_fill_true_color')
            self.del_dxf_attrib('bg_fill_color_name')
        elif color == 'canvas':  # special case for use background color
            self.dxf.bg_fill = const.MTEXT_BG_CANVAS_COLOR
            self.dxf.bg_fill_color = 0  # required but ignored
        else:
            self.dxf.bg_fill = const.MTEXT_BG_COLOR
            if isinstance(color, int):
                self.dxf.bg_fill_color = color
            elif isinstance(color, str):
                self.dxf.bg_fill_color = 0  # required but ignored
                self.dxf.bg_fill_color_name = color
            elif isinstance(color, tuple):
                self.dxf.bg_fill_color = 0  # required but ignored
                self.dxf.bg_fill_true_color = rgb2int(color)
        return self  # fluent interface

    @contextmanager
    def edit_data(self) -> 'MTextData':
        buffer = MTextData(self.get_text())
        yield buffer
        self.set_text(buffer.text)

    buffer = edit_data  # alias


##################################################
# MTEXT inline codes
# \L	Start underline
# \l	Stop underline
# \O	Start overstrike
# \o	Stop overstrike
# \K	Start strike-through
# \k	Stop strike-through
# \P	New paragraph (new line)
# \pxi	Control codes for bullets, numbered paragraphs and columns
# \X	Paragraph wrap on the dimension line (only in dimensions)
# \Q	Slanting (obliquing) text by angle - e.g. \Q30;
# \H	Text height - e.g. \H3x;
# \W	Text width - e.g. \W0.8x;
# \F	Font selection
#
#     e.g. \Fgdt;o - GDT-tolerance
#     e.g. \Fkroeger|b0|i0|c238|p10 - font Kroeger, non-bold, non-italic, codepage 238, pitch 10
#
# \S	Stacking, fractions
#
#     e.g. \SA^B:
#     A
#     B
#     e.g. \SX/Y:
#     X
#     -
#     Y
#     e.g. \S1#4:
#     1/4
#
# \A	Alignment
#
#     \A0; = bottom
#     \A1; = center
#     \A2; = top
#
# \C	Color change
#
#     \C1; = red
#     \C2; = yellow
#     \C3; = green
#     \C4; = cyan
#     \C5; = blue
#     \C6; = magenta
#     \C7; = white
#
# \T	Tracking, char.spacing - e.g. \T2;
# \~	Non-wrapping space, hard space
# {}	Braces - define the text area influenced by the code
# \	Escape character - e.g. \\ = "\", \{ = "{"
#
# Codes and braces can be nested up to 8 levels deep


class MTextData:
    UNDERLINE_START = '\\L;'
    UNDERLINE_STOP = '\\l;'
    UNDERLINE = UNDERLINE_START + '%s' + UNDERLINE_STOP
    OVERSTRIKE_START = '\\O;'
    OVERSTRIKE_STOP = '\\o;'
    OVERSTRIKE = OVERSTRIKE_START + '%s' + OVERSTRIKE_STOP
    STRIKE_START = '\\K;'
    STRIKE_STOP = '\\k;'
    STRIKE = STRIKE_START + '%s' + STRIKE_STOP
    NEW_LINE = '\\P;'
    GROUP_START = '{'
    GROUP_END = '}'
    GROUP = GROUP_START + '%s' + GROUP_END
    NBSP = '\\~'  # none breaking space

    def __init__(self, text: str):
        self.text = text

    def __iadd__(self, text: str) -> 'MTextData':
        self.text += text
        return self

    append = __iadd__

    def set_font(self, name: str, bold: bool = False, italic: bool = False, codepage: int = 1252,
                 pitch: int = 0) -> None:
        bold_flag = 1 if bold else 0
        italic_flag = 1 if italic else 0
        s = "\\F{}|b{}|i{}|c{}|p{};".format(name, bold_flag, italic_flag, codepage, pitch)
        self.append(s)

    def set_color(self, color_name: str) -> None:
        self.append("\\C%d" % const.MTEXT_COLOR_INDEX[color_name.lower()])


def split_string_in_chunks(s: str, size: int = 250) -> List[str]:
    chunks = []
    pos = 0
    while True:
        chunk = s[pos:pos + size]
        chunk_len = len(chunk)
        if chunk_len:
            chunks.append(chunk)
            if chunk_len < size:
                return chunks
            pos += size
        else:
            return chunks
