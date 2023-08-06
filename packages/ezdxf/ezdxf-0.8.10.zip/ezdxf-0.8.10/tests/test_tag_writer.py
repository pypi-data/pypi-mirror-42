# Copyright (c) 2010-2018 Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals

from io import StringIO
from ezdxf.lldxf.tagwriter import TagWriter
from ezdxf.lldxf.types import DXFTag, DXFVertex
from ezdxf.lldxf.tags import Tags


def setup_stream():
    stream = StringIO()
    tagwriter = TagWriter(stream)
    return stream, tagwriter


def test_write_tag2():
    s, t = setup_stream()
    t.write_tag2(0, 'SECTION')
    result = s.getvalue()
    assert result == '  0\nSECTION\n'


def test_write_tag():
    s, t = setup_stream()
    t.write_tag(DXFTag(0, 'SECTION'))
    result = s.getvalue()
    assert result == '  0\nSECTION\n'


def test_write_point_tag():
    s, t = setup_stream()
    t.write_tag(DXFVertex(10, (7., 8., 9.)))
    result = s.getvalue()
    assert result == ' 10\n7.0\n 20\n8.0\n 30\n9.0\n'


def test_write_str():
    s, t = setup_stream()
    t.write_str(' 10\n7.0\n 20\n8.0\n 30\n9.0\n')
    result = s.getvalue()
    assert result == ' 10\n7.0\n 20\n8.0\n 30\n9.0\n'


def test_write_anything():
    s, t = setup_stream()
    t.write_str('... writes just any nonsense ...')
    result = s.getvalue()
    assert result == '... writes just any nonsense ...'


def test_dont_write_5_handles():
    s, t = setup_stream()
    t._write_handles = False
    t.write_tags(Tags.from_text('  0\nLINE\n 5\nFF\n 62\n1\n'))
    result = s.getvalue()
    assert result == '  0\nLINE\n 62\n1\n'


def test_dont_write_105_handles_but_keep_group_code_5():
    s, t = setup_stream()
    t._write_handles = False
    t.write_tags(Tags.from_text("  0\nDIMSTYLE\n105\nFF\n  2\nSTANDARD\n 70\n0\n  3\n\n  4\n\n  5\n\n  6\n\n  7\n\n"))
    result = s.getvalue()
    assert result == "  0\nDIMSTYLE\n  2\nSTANDARD\n 70\n0\n  3\n\n  4\n\n  5\n\n  6\n\n  7\n\n"
