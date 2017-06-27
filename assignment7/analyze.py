"""

Read the source code for wiimote_node.py (from the wiimote.py GitHub repository 4 ) and the PyQtGraph documentation 5 .
Install the PyQtGraph Debian package from the website (run dpkg -i <package.deb> as root). Write a small Python application
analyze.py that takes a Bluetooth MAC address as its only parameter. This application should generate a PyQtGraph flowchart
with the following elements:
• a WiiMoteNode.
• a BufferNode (see wiimote_node.py ) for each of the accelerometer channels,
• three PlotWidget s that plot the accelerometer data for each channel and another PlotWidget that displays the output
of the NormalVectorNode (see below)
• a NormalVectorNode (to be implemented by you) that calculates the rotation around one axis from the accelerometer values
of the other two axes and outputs a vector (i.e., two 2D points) that can be plotted by a PlotWidget to indicate the rotation
(see video in GRIPS) - this node should accept accelerometer values on its two input terminals and provide a list/tuple of two
tuples, such as ((0, 0),(1.0,1.0)) on its output terminal.
• a LogNode that reads values (e.g., accelerometer data) from its input terminal and writes them to stdout .
Your application should import wiimote_node.py and use the two nodes defined there.
Hand in the following file:
analyze.py : a Python script that implements this flowchart.

Points
1 The python script has been submitted, is not empty, and does not print out error messages.
2 The script correctly implements and displays a flowchart.
2 The script correctly reads accelerometer data from the Wiimote and plots it.
1 The script is well-structured and follows the Python style guide (PEP 8).
2 The script contains a working NormalVectorNode as described above.
1 The script contains a working LogNode as described above.

"""

#!/usr/bin/env python3
# coding: utf-8
# -*- coding: utf-8 -*-

from pyqtgraph.flowchart import Flowchart, Node
from pyqtgraph.flowchart.library.common import CtrlNode
import pyqtgraph.flowchart.library as fclib
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

import sys
import wiimote
import wiimote_node

class NormalVectorNode(Node):
    """
    a NormalVectorNode (to be implemented by you) that calculates the rotation around one axis from the accelerometer values
of the other two axes and outputs a vector (i.e., two 2D points) that can be plotted by a PlotWidget to indicate the rotation
(see video in GRIPS) - this node should accept accelerometer values on its two input terminals and provide a list/tuple of two
tuples, such as ((0, 0),(1.0,1.0)) on its output terminal.
    """
    pass


class LogNode(Node):
    # a LogNode that reads values (e.g., accelerometer data) from its input terminal and writes them to stdout .

    pass

"""
class BufferNode(CtrlNode):
    # a BufferNode (see wiimote_node.py ) for each of the accelerometer channels,
    pass

fclib.registerNodeType(BufferNode, [('Data',)])


class WiimoteNode(Node):

    def __init__(self, name):
        terminals = {
            'accelX': dict(io='out'),
            'accelY': dict(io='out'),
            'accelZ': dict(io='out'),
        }

        self.wiimote = None
        self._acc_vals = []

        # update timer
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_all_sensors)
        self.update_timer.start(50.0)

        Node.__init__(self, name, terminals=terminals)


    def update_all_sensors(self):
        if self.wiimote is None:
            return
        self._acc_vals = self.wiimote.accelerometer
        self.update()

    # this seems like the output of the node
    def process(self, **kargs):
        x, y, z = self._acc_vals
        return {'accelX': np.array([x]), 'accelY': np.array([y]), 'accelZ': np.array([z])}

fclib.registerNodeType(WiimoteNode, [('Sensor')])
"""


def main():
    addr_hard = 'B8:AE:6E:1B:5B:03'
    name_hard = 'Nintendo RVL-CNT-01-TR'

    input("Press the 'sync' button on the back of your Wiimote Plus " +
          "or buttons (1) and (2) on your classic Wiimote.\n" +
          "Press <return> once the Wiimote's LEDs start blinking.")

    if len(sys.argv) == 1:
        # type of both is str
        # addr, name = wiimote.find()[0]
        addr = addr_hard
        name = name_hard

    elif len(sys.argv) == 2:
        addr = sys.argv[1]
        name = None

    print(("Connecting to %s (%s)" % (name, addr)))


    app = QtGui.QApplication([])
    win = QtGui.QMainWindow()
    win.setWindowTitle('Analyze.py')
    cw = QtGui.QWidget()
    win.setCentralWidget(cw)
    layout = QtGui.QGridLayout()


    # Create an empty flowchart with a single input and output
    fc = Flowchart(terminals={
    })
    w = fc.widget()

    wiimoteNode = fc.createNode('Wiimote')
    wiimoteNode.text.setText("B8:AE:6E:1B:5B:03")

    wiimoteNode.connect_wiimote()

    bufferNode1 = fc.createNode('Buffer')

    pw1 = pg.PlotWidget()
    layout.addWidget(pw1, 0, 0)
    pw1.setYRange(0, 1024)

    # pw1Node = fc.createNode('PlotWidget', pos=(0, -150))
    pw1Node = fc.createNode('PlotWidget')
    pw1Node.setPlot(pw1)

    # fc.connectTerminals(wiimoteNode1['accelX'], bufferNode1['dataIn'])
    # fc.connectTerminals(bufferNode1['dataOut'], pw1Node['In'])
    fc.connectTerminals(wiimoteNode['accelX'], bufferNode1['dataIn'])
    fc.connectTerminals(bufferNode1['dataOut'], pw1Node['In'])



    # wiimoteNode2 = fc.createNode('Wiimote')
    bufferNode2 = fc.createNode('Buffer')

    pw2 = pg.PlotWidget()
    layout.addWidget(pw2, 0, 1)
    pw2.setYRange(0, 1024)

    pw2Node = fc.createNode('PlotWidget')
    pw2Node.setPlot(pw2)

    fc.connectTerminals(wiimoteNode['accelY'], bufferNode2['dataIn'])
    fc.connectTerminals(bufferNode2['dataOut'], pw2Node['In'])



    # wiimoteNode3 = fc.createNode('Wiimote')
    bufferNode3 = fc.createNode('Buffer')

    pw3 = pg.PlotWidget()
    layout.addWidget(pw3, 0, 2)
    pw3.setYRange(0, 1024)

    pw3Node = fc.createNode('PlotWidget')
    pw3Node.setPlot(pw3)

    fc.connectTerminals(wiimoteNode['accelZ'], bufferNode3['dataIn'])
    fc.connectTerminals(bufferNode3['dataOut'], pw3Node['In'])



    wiimoteNode4 = fc.createNode('Wiimote')
    bufferNode4 = fc.createNode('Buffer')

    pw4 = pg.PlotWidget()
    layout.addWidget(pw4, 1, 0, 1, 3)
    pw4.setYRange(0, 1024)

    pw4Node = fc.createNode('PlotWidget')
    pw4Node.setPlot(pw4)

    fc.connectTerminals(wiimoteNode4['accelY'], bufferNode4['dataIn'])
    fc.connectTerminals(bufferNode4['dataOut'], pw4Node['In'])

    layout.setRowStretch(0, 2)

    cw.setLayout(layout)


    win.show()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()


    """
    TODO:
        create a qtapp
        4 PlotWidgets
            3 for the x,y,z axis of the accelerometer
            1 for the normalvectornode


    """




if __name__ == '__main__':
    main()
