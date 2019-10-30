from openheating.dbus import node

import unittest
import xml.etree.ElementTree as ET


class NodeDefinitionTest(unittest.TestCase):

    def test__to_xml(self):
        iface1 = '''
        <interface name='iface1'>
        </interface>
        '''
        iface2 = '''
        <interface name='iface2'>
        </interface>
        '''

        nodedef = node.Definition(interfaces=(iface1, iface2))

        node_et = ET.fromstring(nodedef.to_xml())
        self.assertEqual(node_et.tag, 'node')
        niface1 = niface2 = 0
        for iface in node_et:
            if iface.get('name') == 'iface1':
                niface1 += 1
            if iface.get('name') == 'iface2':
                niface2 += 1
        self.assertEqual(niface1, 1)
        self.assertEqual(niface2, 1)

    def test__apply_to(self):
        nodedef = node.Definition(interfaces=('''
            <interface name='iface'>
            </interface>
            ''',))

        class klass:
            pass

        nodedef(klass)
        self.assertEqual(klass.dbus, nodedef.to_xml())


suite = unittest.defaultTestLoader.loadTestsFromTestCase(NodeDefinitionTest)

if __name__ == '__main__':
    unittest.main()
