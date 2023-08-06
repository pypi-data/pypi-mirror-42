#!/usr/bin/env python
# Created: 12.03.2011, 2018 rewritten for pytest
# Copyright (C) 2011-2018, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
import ezdxf


def test_new_AC1009():
    dwg = ezdxf.new('AC1009')
    assert 'AC1009' == dwg.dxfversion


def test_new_AC1015():
    dwg = ezdxf.new('AC1015')
    assert 'AC1015' == dwg.dxfversion


def test_new_AC1018():
    dwg = ezdxf.new('AC1018')
    assert 'AC1018' == dwg.dxfversion


def test_new_AC1021():
    dwg = ezdxf.new('AC1021')
    assert 'AC1021' == dwg.dxfversion


def test_new_AC1024():
    dwg = ezdxf.new('AC1024')
    assert 'AC1024' == dwg.dxfversion


def test_new_AC1032():
    dwg = ezdxf.new('AC1032')
    assert 'AC1032' == dwg.dxfversion
