#!/usr/bin/env python3
"""Check description structure and binary STL integrity without ROS."""
from pathlib import Path
import struct
import xml.etree.ElementTree as ET

package = Path(__file__).resolve().parents[1]
robot = ET.parse(package / 'urdf/robot.urdf').getroot()
links = {e.attrib['name'] for e in robot.findall('link')}
joints = robot.findall('joint')
children = [j.find('child').attrib['link'] for j in joints]
assert len(children) == len(set(children))
assert links - set(children) == {'world'}
reached = {'world'}
pending = list(joints)
while pending:
    count = len(pending)
    for joint in pending[:]:
        parent = joint.find('parent').attrib['link']
        child = joint.find('child').attrib['link']
        assert parent in links and child in links
        if parent in reached:
            reached.add(child)
            pending.remove(joint)
    assert len(pending) < count, 'Disconnected or cyclic tree'
for mesh in robot.findall('.//mesh'):
    prefix = 'package://robotic_arm_description/'
    assert mesh.attrib['filename'].startswith(prefix)
    path = package / mesh.attrib['filename'][len(prefix):]
    data = path.read_bytes()
    count = struct.unpack_from('<I', data, 80)[0]
    assert count > 0 and len(data) == 84 + count * 50
print(f'Valid tree: {len(links)} links, {len(joints)} joints. All mesh references resolve.')
