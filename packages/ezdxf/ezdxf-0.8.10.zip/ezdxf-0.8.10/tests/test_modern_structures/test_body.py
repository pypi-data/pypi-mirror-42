# Created: 03.05.2014, 2018 rewritten for pytest
# Copyright (C) 2014-2018, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
import pytest
import ezdxf


@pytest.fixture(scope='module')
def layout():
    dwg = ezdxf.new('AC1024')
    return dwg.modelspace()


def test_body_default_settings(layout):
    body = layout.add_body()
    assert '0' == body.dxf.layer


def test_body_getting_acis_data(layout):
    body = layout.add_body(acis_data=TEST_DATA.splitlines())
    assert TEST_DATA == "\n".join(body.get_acis_data())


def test_body_acis_data_context_manager(layout):
    body = layout.add_body()
    with body.edit_data() as data:
        data.text_lines.extend(TEST_DATA.splitlines())
    data = list(body.get_acis_data())
    assert TEST_DATA == "\n".join(data)


def test_region_default_settings(layout):
    region = layout.add_region()
    assert '0' == region.dxf.layer


def test_region_getting_acis_data(layout):
    region = layout.add_region(acis_data=TEST_DATA.splitlines())
    assert TEST_DATA == "\n".join(region.get_acis_data())


def test_3dsolid_default_settings(layout):
    _3dsolid = layout.add_3dsolid()
    assert '0' == _3dsolid.dxf.layer
    assert '0' == _3dsolid.dxf.history


def test_3dsolid_getting_acis_data(layout):
    _3dsolid = layout.add_3dsolid(acis_data=TEST_DATA.splitlines())
    assert TEST_DATA == "\n".join(_3dsolid.get_acis_data())


TEST_DATA = """21200 115 2 26
16 Autodesk AutoCAD 19 ASM 217.0.0.4503 NT 0
1 9.9999999999999995e-007 1e-010
asmheader $-1 -1 @12 217.0.0.4503 #
body $2 -1 $-1 $3 $-1 $-1 #
ref_vt-eye-attrib $-1 -1 $-1 $-1 $1 $4 $5 #
lump $6 -1 $-1 $-1 $7 $1 #
eye_refinement $-1 -1 @5 grid  1 @3 tri 1 @4 surf 0 @3 adj 0 @4 grad 0 @9 postcheck 0 @4 stol 0.020115179941058159 @4 ntol 30 @4 dsil 0 @8 flatness 0 @7 pixarea 0 @4 hmax 0 @6 gridar 0 @5 mgrid 3000 @5 ugrid 0 @5 vgrid 0 @10 end_fields #
vertex_template $-1 -1 3 0 1 8 #"""
