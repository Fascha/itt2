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

import sys
import wiimote_node



def main():
    pass

if __name__ == '__main__':
    main()
