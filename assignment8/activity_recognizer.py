"""

8.1: Activity Recognition
Implement a Python application that allows the user to record a set of different gestures or activities (standing, sitting, running,
shaking the Wiimote, throwing it, etc.) and distinguish between them using data from the Wiimote’s accelerometer.
Specifically, implement the following as a PyQtGraph flowchart:
• a graphical user interface where the user can add new gestures and record examples for these gestures using the Wiimote
• a feature-extraction filter that extracts useful information from the raw values (e.g., FFT, stddev, derivatives)
• a machine-learning classifier (e.g., a SVM) that is trained on the example gestures whenever a new example gesture is recorded
• a mode where the user can execute one of the trained gestures with the Wiimote and the system recognizes it.
• optional but helpful: allow the user to remove and retrain gestures.
The individual nodes of the flowchart should be reusable and modular, and should have sensible interfaces (i.e., input and output
terminals pass appropriate values, such as lists or integers; no use of application-global variables). Experiment with different sets
of gestures and find a few that can be distinguished well.

Example implementation:
implement an FftNode that reads in information from a BufferNode and outputs a frequency spectrogram.
Furthermore, implement an SvmNode that can be switched between training mode and prediction mode and “inactive”
via buttons in the configuration pane (see WiimoteNode and BufferNode for examples). In training mode it continually reads in a
sample (i.e. a feature vector consisting of multiple values, such as a list of frequency components) and trains a SVM classifier with
this data (and previous data). The category for this sample can be defined by a text field in the control pane.In prediction mode
the SvmNode should read in a sample and output the predicted category as a string. Implement a DisplayTextNode that displays
the currently recognized/predicted category on the screen.
Hand in the following file:
activity_recognizer.py : a Python file implementing your solution.
Hand in further helper files (incl. wiimote.py, etc.) as needed.


Points
1 The python script has been submitted, is not empty, and does not print out error messages.
1 The script is well-structured and follows the Python style guide (PEP 8).
1 The script is well documented.
3 The script correctly implements the features above.
1 The flowchart nodes have sensible interfaces.
2 The script accurately detects 3 different gestures.
2 Training and prediction work in real time
2 The user interface for training and prediction is user-friendly and visually pleasant

"""

from pyqtgraph.flowchart import Flowchart, Node
from pyqtgraph.flowchart.library.common import CtrlNode
import pyqtgraph.flowchart.library as fclib
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

import wiimote
# import wiimote_node
import sys

from scipy import fft


class BufferNode(CtrlNode):
    """
    Buffers the last n samples provided on input and provides them as a list of
    length n on output.
    A spinbox widget allows for setting the size of the buffer.
    Default size is 32 samples.
    """
    nodeName = "Buffer"
    uiTemplate = [
        ('size',  'spin', {'value': 32.0, 'step': 1.0, 'bounds': [0.0, 128.0]}),
    ]

    def __init__(self, name):
        terminals = {
            'dataIn': dict(io='in'),
            'dataOut': dict(io='out'),
        }
        self._buffer = np.array([])
        CtrlNode.__init__(self, name, terminals=terminals)

    def process(self, **kwds):
        size = int(self.ctrls['size'].value())
        self._buffer = np.append(self._buffer, kwds['dataIn'])
        self._buffer = self._buffer[-size:]
        output = self._buffer
        return {'dataOut': output}

fclib.registerNodeType(BufferNode, [('Data',)])


class WiimoteNode(Node):
    """
    Outputs sensor data from a Wiimote.

    Supported sensors: accelerometer (3 axis)
    Text input box allows for setting a Bluetooth MAC address.
    Pressing the "connect" button tries connecting to the Wiimote.
    Update rate can be changed via a spinbox widget. Setting it to "0"
    activates callbacks every time a new sensor value arrives (which is
    quite often -> performance hit)
    """

    nodeName = "Wiimote"

    def __init__(self, name):
        terminals = {
            'accelX': dict(io='out'),
            'accelY': dict(io='out'),
            'accelZ': dict(io='out'),
        }
        self.wiimote = None
        self._acc_vals = []

        # # Configuration UI
        # self.ui = QtGui.QWidget()
        # self.layout = QtGui.QGridLayout()
        #
        # label = QtGui.QLabel("Bluetooth MAC address:")
        # self.layout.addWidget(label)
        #
        # self.text = QtGui.QLineEdit()
        # self.btaddr = "b8:ae:6e:18:5d:ab"  # set some example
        # self.text.setText(self.btaddr)
        # self.layout.addWidget(self.text)
        #
        # label2 = QtGui.QLabel("Update rate (Hz)")
        # self.layout.addWidget(label2)
        #
        # self.update_rate_input = QtGui.QSpinBox()
        # self.update_rate_input.setMinimum(0)
        # self.update_rate_input.setMaximum(60)
        # self.update_rate_input.setValue(20)
        # self.update_rate_input.valueChanged.connect(self.set_update_rate)
        # self.layout.addWidget(self.update_rate_input)
        #
        # self.connect_button = QtGui.QPushButton("connect")
        # self.connect_button.clicked.connect(self.connect_wiimote)
        # self.layout.addWidget(self.connect_button)
        # self.ui.setLayout(self.layout)

        # update timer
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_all_sensors)

        # super()
        Node.__init__(self, name, terminals=terminals)

    def update_all_sensors(self):
        if self.wiimote is None:
            return
        self._acc_vals = self.wiimote.accelerometer
        # todo: other sensors...
        self.update()

    def update_accel(self, acc_vals):
        self._acc_vals = acc_vals
        self.update()

    # def ctrlWidget(self):
    #     return self.ui

    def connect_wiimote(self, btaddr, model=None):
        # self.btaddr = str(self.text.text()).strip()
        if self.wiimote is not None:
            self.wiimote.disconnect()
            self.wiimote = None
            # self.connect_button.setText("connect")
            return
        if len(btaddr) == 17:
            # self.connect_button.setText("connecting...")
            if model:
                self.wiimote = wiimote.connect(btaddr, model)
            else:
                self.wiimote = wiimote.connect(btaddr)
            if self.wiimote is None:
                self.connect_button.setText("try again")
            else:
                # self.connect_button.setText("disconnect")
                # self.set_update_rate(self.update_rate_input.value())
                self.set_update_rate(60)

    def set_update_rate(self, rate):
        if rate == 0:  # use callbacks for max. update rate
            self.update_timer.stop()
            self.wiimote.accelerometer.register_callback(self.update_accel)
        else:
            self.wiimote.accelerometer.unregister_callback(self.update_accel)
            self.update_timer.start(1000.0/rate)

    def process(self, **kwdargs):
        x, y, z = self._acc_vals
        return {'accelX': np.array([x]), 'accelY': np.array([y]), 'accelZ': np.array([z])}

fclib.registerNodeType(WiimoteNode, [('Sensor',)])


class FftNode(Node):
    """
    implement an FftNode that reads in information from a BufferNode and outputs a frequency spectrogram.
    """

    nodeName = 'Fft'

    def __init__(self, name):
        terminals = {
            'inX': dict(io='in'),
            'inY': dict(io='in'),
            'inZ': dict(io='in'),
            'fft': dict(io='out')
        }
        Node.__init__(self, name, terminals=terminals)

    def process(self, **kwds):
        x = kwds['inX']
        y = kwds['inY']
        z = kwds['inZ']

        avg = (x + y + z)/3
        print(avg)

        freq = [np.abs(fft(avg)/len(avg))[1:len(avg)//2]]

        print(freq)

        return {'fft': freq}


fclib.registerNodeType(FftNode, [('Custom',)])


class SvmNode(Node):
    """
    implement an SvmNode that can be switched between training mode and prediction mode and “inactive”
    via buttons in the configuration pane (see WiimoteNode and BufferNode for examples). In training mode it continually reads in a
    sample (i.e. a feature vector consisting of multiple values, such as a list of frequency components) and trains a SVM classifier with
    this data (and previous data).

    """

    nodeName = 'Svm'

    def __init__(self, name):
        terminals = {

        }
        Node.__init__(self, name, terminals=terminals)

    def process(self, **kwds):
        pass


fclib.registerNodeType(SvmNode, [('Custom'),])


class RecordNode(Node):

    nodeName = 'Record'




class ActivityRecognition():

    RED = QtGui.QColor(255, 0, 0)
    GREEN = QtGui.QColor(0, 255, 0)
    YELLOW = QtGui.QColor(255, 255, 0)
    GRAY = QtGui.QColor(100, 100, 100)

    def __init__(self, app):
        self.app = app

        self.training_mode = False

        self.init_ui()
        self.setup_nodes()
        self.connect_buttons()

        self.win.show()
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def init_ui(self):
        width, height = self.app.desktop().width(), self.app.desktop().height()

        print("5")
        self.win = QtGui.QWidget()
        self.win.setWindowTitle('Activity Recognition')
        self.win.setGeometry(width/4, height/4, width/2, height/2)

        self.main_layout = QtGui.QGridLayout()
        self.win.setLayout(self.main_layout)

        print("6")
        self.setup_left_group()
        print("7")
        self.setup_middle_group()
        print("8")
        self.setup_right_group()
        print("9")


    def setup_left_group(self):

        left_group = QtGui.QGroupBox()
        left_layout = QtGui.QGridLayout()

        wm_label = QtGui.QLabel("Enter your mac address")
        self.wm_addr = QtGui.QLineEdit()
        self.wm_addr.setPlaceholderText("Enter your mac address here")
        self.wm_addr.setText("B8:AE:6E:1B:5B:03")
        self.wm_connect_btn = QtGui.QPushButton("Connect")
        # wm_connect_btn.clicked.connect(self.connect_wm)

        left_layout.addWidget(wm_label, 1, 1, 1, 2)
        left_layout.addWidget(self.wm_addr, 2, 1, 1, 2)
        left_layout.addWidget(self.wm_connect_btn, 3, 1, 1, 2)


        self.training_hint = QtGui.QLabel("You can toggle Training Mode by pressing 'A' on your WiiMote!")

        self.training_label = QtGui.QLabel("NO WIIMOTE CONNECTED")
        self.training_label.setAlignment(QtCore.Qt.AlignCenter)
        self.training_label.setAutoFillBackground(True)
        self.training_btn = QtGui.QPushButton("Activate Training Mode")
        # self.training_btn.clicked.connect(self.toggle_training_mode)


        left_layout.addWidget(self.training_hint, 4, 1, 1, 2)
        left_layout.addWidget(self.training_label, 5, 1, 1, 2)
        left_layout.addWidget(self.training_btn, 6, 1, 1, 2)


        left_group.setLayout(left_layout)
        self.main_layout.addWidget(left_group, 1, 1, 1, 1)

    def setup_middle_group(self):

        middle_group = QtGui.QGroupBox()
        middle_layout = QtGui.QGridLayout()

        l1 = QtGui.QLabel()
        l1.setText("MIDDLE GROUP")
        middle_layout.addWidget(l1, 1, 1)

        self.spectrogram_widget = pg.PlotWidget()
        middle_layout.addWidget(self.spectrogram_widget, 2, 1)

        middle_group.setLayout(middle_layout)
        self.main_layout.addWidget(middle_group, 1, 2, 1, 5)

    def setup_right_group(self):
        right_group = QtGui.QGroupBox()
        right_layout = QtGui.QGridLayout()

        self.connected_status_label = QtGui.QLabel()
        self.connected_status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.connected_status_label.setAutoFillBackground(True)

        connected_status_palette = self.connected_status_label.palette()
        connected_status_palette.setColor(self.connected_status_label.backgroundRole(), self.RED)
        self.connected_status_label.setPalette(connected_status_palette)

        self.connected_status_label.setText("NOT CONNECTED")
        right_layout.addWidget(self.connected_status_label, 1, 1)

        self.recording_status_label = QtGui.QLabel()
        self.recording_status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.recording_status_label.setAutoFillBackground(True)

        recording_status_palette = self.recording_status_label.palette()
        recording_status_palette.setColor(self.recording_status_label.backgroundRole(), self.RED)
        self.recording_status_label.setPalette(recording_status_palette)

        self.recording_status_label.setText("NOT RECORDING")
        right_layout.addWidget(self.recording_status_label, 2, 1)


        self.available_gestures = QtGui.QLabel()
        self.available_gestures.setText("HERE WILL BE AVAILABLE GESTURES")
        right_layout.addWidget(self.available_gestures, 2, 1, 3, 1)

        right_group.setLayout(right_layout)
        self.main_layout.addWidget(right_group, 1, 7, 1, 1)

    def setup_nodes(self):
        # Create an empty flowchart with a single input and output
        print("1")
        self.fc = Flowchart(terminals={})

        self.wiimote_node = self.fc.createNode('Wiimote')

        self.buffer_node_x = self.fc.createNode('Buffer')
        self.buffer_node_y = self.fc.createNode('Buffer')
        self.buffer_node_z = self.fc.createNode('Buffer')

        self.fft_node = self.fc.createNode('Fft')
        print("2")
        self.fc.connectTerminals(self.wiimote_node['accelX'], self.buffer_node_x['dataIn'])
        self.fc.connectTerminals(self.wiimote_node['accelY'], self.buffer_node_y['dataIn'])
        self.fc.connectTerminals(self.wiimote_node['accelZ'], self.buffer_node_z['dataIn'])

        self.fc.connectTerminals(self.buffer_node_x['dataOut'], self.fft_node['inX'])
        self.fc.connectTerminals(self.buffer_node_y['dataOut'], self.fft_node['inY'])
        self.fc.connectTerminals(self.buffer_node_z['dataOut'], self.fft_node['inZ'])

        print("3")

        spectrogram_node = self.fc.createNode('PlotWidget')
        spectrogram_node.setPlot(self.spectrogram_widget)

        self.fc.connectTerminals(self.fft_node['fft'], spectrogram_node['In'])
        print("4")

    def connect_buttons(self):
        print("connect buttons def start")
        self.training_btn.clicked.connect(self.toggle_training_mode)
        self.wm_connect_btn.clicked.connect(self.connect_wm)

        print("connect buttons def end")

    def connect_wm(self):
        print("connect wm def")
        btaddr = self.wm_addr.text().strip()
        print(btaddr)
        self.wiimote_node.connect_wiimote(btaddr, model='Nintendo RVL-CNT-01-TR')

        self.training_label.setText("Training Mode OFF")
        self.connected_status_label.setText("CONNECTED")
        connected_status_palette = self.connected_status_label.palette()
        connected_status_palette.setColor(self.connected_status_label.backgroundRole(), self.GREEN)
        self.connected_status_label.setPalette(connected_status_palette)

        self.wiimote_node.wiimote.buttons.register_callback(self.handle_wm_button)

    def handle_wm_button(self, buttons):
        if len(buttons) > 0:
            print(buttons)
            for button in buttons:
                if button[0] == 'A':
                    if button[1]:
                        self.toggle_training_mode()

    def toggle_training_mode(self):
        self.training_mode = not self.training_mode
        print('New State (Training Mode): ', self.training_mode)
        if self.training_mode:
            self.training_btn.setText("Deactivate Training Mode")
            self.training_label.setText("Training Mode ON")
            training_status_palette = self.training_label.palette()
            training_status_palette.setColor(self.training_label.backgroundRole(), self.YELLOW)
            self.training_label.setPalette(training_status_palette)
        else:
            self.training_btn.setText("Activate Training Mode")
            self.training_label.setText("Training Mode OFF")
            training_status_palette = self.training_label.palette()
            training_status_palette.setColor(self.training_label.backgroundRole(), self.GRAY)
            self.training_label.setPalette(training_status_palette)


def main():
    app = QtGui.QApplication([])

    activity_recognition = ActivityRecognition(app)


if __name__ == '__main__':
    main()
