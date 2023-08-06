# Created: 11.12.2018
# Copyright (c) 2018, Manfred Moitzi
# License: MIT License
"""
ezdxf typing collection

Only usable in type checking mode:

if TYPE_CHECKING:
    from ezdxf.eztypes import DXFTag

"""
from typing import *

if TYPE_CHECKING:
    # Low level stuff
    from ezdxf.math.vector import Vector, Vec2
    from ezdxf.math.matrix44 import Matrix44
    from ezdxf.math.bbox import BoundingBox, BoundingBox2d
    from ezdxf.tools.handle import HandleGenerator
    from ezdxf.lldxf.types import DXFTag, DXFBinaryTag, DXFVertex
    from ezdxf.lldxf.attributes import XType, DXFAttr
    from ezdxf.lldxf.tags import Tags
    from ezdxf.lldxf.extendedtags import ExtendedTags
    from ezdxf.lldxf.tagwriter import TagWriter
    from ezdxf.tools.complex_ltype import ComplexLineTypePart

    # Entity factories
    from ezdxf.legacy.factory import LegacyDXFFactory
    from ezdxf.modern.factory import ModernDXFFactory

    from ezdxf.legacy.layouts import DXF12Layout, DXF12BlockLayout
    from ezdxf.modern.layouts import Layout, BlockLayout

    # Entities manager
    from ezdxf.entityspace import EntitySpace
    from ezdxf.drawing import Drawing
    from ezdxf.database import EntityDB

    # Sections and Tables
    from ezdxf.sections.table import Table, ViewportTable
    from ezdxf.sections.blocks import BlocksSection
    from ezdxf.sections.header import HeaderSection
    from ezdxf.sections.tables import TablesSection
    from ezdxf.sections.blocks import BlocksSection
    from ezdxf.sections.classes import ClassesSection
    from ezdxf.sections.objects import ObjectsSection
    from ezdxf.sections.entities import EntitySection
    from ezdxf.sections.unsupported import UnsupportedSection

    # Table entries
    from ezdxf.modern.tableentries import BlockRecord, Layer, Linetype, Style, DimStyle
    from ezdxf.modern.tableentries import UCS, View, AppID, VPort

    # Style Manager
    from ezdxf.modern.dxfgroups import GroupManager
    from ezdxf.modern.material import MaterialManager
    from ezdxf.modern.mleader import MLeaderStyleManager
    from ezdxf.modern.mline import MLineStyleManager
    from ezdxf.dimstyleoverride import DimStyleOverride

    # DXF objects
    from ezdxf.modern.dxfobjects import DXFObject
    from ezdxf.modern.dxfdict import DXFDictionary
    from ezdxf.modern.geodata import GeoData
    from ezdxf.modern.sortentstable import SortEntitiesTable

    # DXF entities
    from ezdxf.dxfentity import DXFEntity
    from ezdxf.legacy.graphics import Line, Point, Circle, Arc, Shape
    from ezdxf.legacy.trace import Solid, Trace, Face
    from ezdxf.legacy.polyline import Polyline, Polyface, Polymesh, DXFVertex
    from ezdxf.legacy.insert import Insert
    from ezdxf.legacy.attrib import Attdef, Attrib
    from ezdxf.legacy.dimension import Dimension
    from ezdxf.legacy.text import Text

    from ezdxf.modern.spline import Spline
    from ezdxf.modern.viewport import Viewport
    from ezdxf.modern.block import Block
    from ezdxf.modern.image import ImageDef, Image
    from ezdxf.modern.underlay import UnderlayDef, Underlay
    from ezdxf.modern.mesh import Mesh
    from ezdxf.modern.hatch import Hatch
    from ezdxf.modern.lwpolyline import LWPolyline
    from ezdxf.modern.ellipse import Ellipse
    from ezdxf.modern.ray import Ray, XLine
    from ezdxf.modern.mtext import MText
    from ezdxf.modern.solid3d import Solid3d, Body, Region
    from ezdxf.modern.surface import Surface, ExtrudedSurface, RevolvedSurface, LoftedSurface, SweptSurface
    from ezdxf.render.dimension import BaseDimensionRenderer

    # other
    from ezdxf.audit import Auditor
    from ezdxf.lldxf.tags import DXFInfo

    # Type compositions
    Vertex = Union[Sequence[float], Vector, Vec2]
    VecXY = Union[Vec2, Vector]  # Vector with x and y attributes
    TagValue = Union[str, int, float, Sequence[float], Vector]
    RGB = Tuple[int, int, int]
    IterableTags = Iterable[Tuple[int, TagValue]]
    SectionDict = Dict[str, List[Union[Tags, ExtendedTags]]]
    KeyFunc = Callable[['DXFEntity'], Hashable]
    FaceType = Sequence[Vertex]

    # Type Unions
    DXFFactoryType = Union[LegacyDXFFactory, ModernDXFFactory]
    LayoutType = Union[DXF12Layout, Layout]
    BlockLayoutType = Union[DXF12BlockLayout, BlockLayout]
    GenericLayoutType = Union[LayoutType, BlockLayoutType]
    SectionType = Union[
        HeaderSection, TablesSection, BlocksSection, ClassesSection, ObjectsSection, EntitySection, UnsupportedSection]
