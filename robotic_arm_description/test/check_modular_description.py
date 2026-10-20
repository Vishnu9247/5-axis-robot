#!/usr/bin/env python3
"""Expand the modular source and verify it matches the plain URDF compatibility copy."""
from pathlib import Path
import xml.etree.ElementTree as ET
import xacro

package = Path(__file__).resolve().parents[1]
def signature(element):
    return (element.tag, tuple(sorted(element.attrib.items())),
            tuple(signature(child) for child in element))
def members(root):
    return {(element.tag, element.attrib['name']): signature(element)
            for element in root if element.tag in ('link', 'joint')}
expanded = ET.fromstring(xacro.process_file(str(package / 'urdf/robot.urdf.xacro')).toxml())
plain = ET.parse(package / 'urdf/robot.urdf').getroot()
assert members(expanded) == members(plain), 'Plain URDF is out of date; regenerate it with Xacro.'
print('Modular source and plain URDF describe exactly the same links and joints.')
