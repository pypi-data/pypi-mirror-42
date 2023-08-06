# Purpose: 'mtext' example
# Created: 18.02.2017
# Copyright (c) 2017 Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
import ezdxf

dwg = ezdxf.new('ac1015')
modelspace = dwg.modelspace()
modelspace.add_mtext("This is a text in the YZ-plane",
                     dxfattribs={
                         'width': 12,  # reference rectangle width
                         'text_direction': (0, 1, 0),  # write in y direction
                         'extrusion': (1, 0, 0)  # normal vector of the text plane
                     })

dwg.saveas('mtext_in_yz_plane.dxf')

