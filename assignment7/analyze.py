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
    nach oben:
        500 500 600

    nach rechts:
        600 500 500

    nach unten:
        500 500 400

    nach links:
        400 500 500
    """

    nodeName = "Normalvector"

    def __init__(self, name):
        terminals = {
            'accelX': dict(io='in'),
            'accelZ': dict(io='in'),
            'normalX': dict(io='out'),
            'normalY': dict(io='out')
        }
        Node.__init__(self, name, terminals=terminals)

    def process(self, **kwds):
        x = kwds['accelX']
        z = kwds['accelZ']

        diffx = (612 - x)/200
        diffz = (z - 508)/200

        return {'normalX': [0, float(np.cos(diffx*np.pi))], 'normalY': [0, float(np.sin(diffz*np.pi))]}


fclib.registerNodeType(NormalVectorNode, [('Data',)])


class LogNode(Node):
    # a LogNode that reads values (e.g., accelerometer data) from its input terminal and writes them to stdout .

    nodeName = 'Log'

    def __init__(self, name):
        terminals = {
            'accelX': dict(io='in'),
            'accelY': dict(io='in'),
            'accelZ': dict(io='in')
        }
        Node.__init__(self, name, terminals=terminals)

    def process(self, **kwds):
        print("%d, %d, %d" % (kwds['accelX'], kwds['accelY'], kwds['accelZ']))


fclib.registerNodeType(LogNode, [('Data',)])


def main():
    addr_hard = 'B8:AE:6E:1B:5B:03'
    name_hard = 'Nintendo RVL-CNT-01-TR'

    input("Press the 'sync' button on the back of your Wiimote Plus " +
          "or buttons (1) and (2) on your classic Wiimote.\n" +
          "Press <return> once the Wiimote's LEDs start blinking.")

    # use hardcoded addr if no parameters were given
    # for easier testing
    if len(sys.argv) == 1:
        addr = addr_hard
        name = name_hard

    elif len(sys.argv) == 2:
        addr = sys.argv[1]
        name = None

    print(("Connecting to %s (%s)" % (name, addr)))

    # Initializing UI
    app = QtGui.QApplication([])
    win = QtGui.QMainWindow()
    win.setWindowTitle('Analyze.py')
    cw = QtGui.QWidget()
    win.setCentralWidget(cw)
    layout = QtGui.QGridLayout()
    layout.setRowStretch(0, 2)
    cw.setLayout(layout)

    # Create an empty flowchart with a single input and output
    fc = Flowchart(terminals={
    })
    w = fc.widget()

    layout.addWidget(w, 0, 0, 2, 1)

    # Init WiimoteNode and connect Wiimote via bluetooth
    wiimoteNode = fc.createNode('Wiimote', pos=(-300, 0))
    wiimoteNode.text.setText(addr)

    wiimoteNode.connect_wiimote()

    # X-Axis Plot
    bufferNode1 = fc.createNode('Buffer', pos=(0, -200))

    pw1 = pg.PlotWidget()
    layout.addWidget(pw1, 0, 1)
    pw1.setYRange(0, 1024)

    pw1Node = fc.createNode('PlotWidget', pos=(150, -200))
    pw1Node.setPlot(pw1)

    fc.connectTerminals(wiimoteNode['accelX'], bufferNode1['dataIn'])
    fc.connectTerminals(bufferNode1['dataOut'], pw1Node['In'])

    # Y-Axis Plot
    bufferNode2 = fc.createNode('Buffer', pos=(0, -50))

    pw2 = pg.PlotWidget()
    layout.addWidget(pw2, 0, 2)
    pw2.setYRange(0, 1024)

    pw2Node = fc.createNode('PlotWidget', pos=(150, -50))
    pw2Node.setPlot(pw2)

    fc.connectTerminals(wiimoteNode['accelY'], bufferNode2['dataIn'])
    fc.connectTerminals(bufferNode2['dataOut'], pw2Node['In'])

    # Z-Axis Plot
    bufferNode3 = fc.createNode('Buffer', pos=(0, 100))

    pw3 = pg.PlotWidget()
    layout.addWidget(pw3, 0, 3)
    pw3.setYRange(0, 1024)

    pw3Node = fc.createNode('PlotWidget', pos=(150, 100))
    pw3Node.setPlot(pw3)

    fc.connectTerminals(wiimoteNode['accelZ'], bufferNode3['dataIn'])
    fc.connectTerminals(bufferNode3['dataOut'], pw3Node['In'])

    # Normalvector
    normalNode = fc.createNode('Normalvector', pos=(-150, 250))
    curveNode = fc.createNode('PlotCurve', pos=(0, 250))

    pw4 = pg.PlotWidget()
    pw4.setYRange(-2, 2)
    pw4.setXRange(-2, 2)
    layout.addWidget(pw4, 1, 1, 1, 3)
    pw4Node = fc.createNode('PlotWidget', pos=(150, 250))

    pw4Node.setPlot(pw4)

    fc.connectTerminals(wiimoteNode['accelX'], normalNode['accelX'])
    fc.connectTerminals(wiimoteNode['accelZ'], normalNode['accelZ'])
    fc.connectTerminals(normalNode['normalX'], curveNode['x'])
    fc.connectTerminals(normalNode['normalY'], curveNode['y'])
    fc.connectTerminals(curveNode['plot'], pw4Node['In'])

    # Lognode
    logNode = fc.createNode('Log', pos=(-150, -300))

    fc.connectTerminals(wiimoteNode['accelX'], logNode['accelX'])
    fc.connectTerminals(wiimoteNode['accelY'], logNode['accelY'])
    fc.connectTerminals(wiimoteNode['accelZ'], logNode['accelZ'])

    win.show()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()


if __name__ == '__main__':
    main()
