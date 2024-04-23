import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class ParameterSettingsWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("参数设置")
        self.setFixedSize(300, 150)

        layout = QtWidgets.QVBoxLayout()

        self.iou_label = QtWidgets.QLabel("IoU阈值：")
        layout.addWidget(self.iou_label)
        self.iou_spinbox = QtWidgets.QDoubleSpinBox()
        self.iou_spinbox.setMinimum(0)
        self.iou_spinbox.setMaximum(1)
        layout.addWidget(self.iou_spinbox)

        self.confidence_label = QtWidgets.QLabel("置信度阈值：")
        layout.addWidget(self.confidence_label)
        self.confidence_spinbox = QtWidgets.QDoubleSpinBox()
        self.confidence_spinbox.setMinimum(0)
        self.confidence_spinbox.setMaximum(1)
        layout.addWidget(self.confidence_spinbox)

        self.ok_button = QtWidgets.QPushButton("确定")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("鱼道智能生态监测系统")

        # 创建左侧按钮
        self.button_layout = QtWidgets.QVBoxLayout()

        self.create_button("过鱼视频文件路径", self.select_video_path)
        self.create_button("加载细粒度检测模型权重", self.select_fine_model)
        self.create_button("加载粗粒度检测模型权重", self.select_coarse_model)
        self.create_button("加载目标追踪模型权重", self.select_tracking_model)
        self.create_button("参数设置", self.show_parameter_settings)
        self.create_button("开始检测", self.start_detection)

        left_widget = QtWidgets.QWidget()
        left_widget.setLayout(self.button_layout)

        monitoring_groupbox_left = QtWidgets.QGroupBox("控制区")
        monitoring_layout_left = QtWidgets.QVBoxLayout()
        monitoring_layout_left.addWidget(left_widget)
        monitoring_groupbox_left.setLayout(monitoring_layout_left)

        # 创建监测窗口和当前过鱼信息
        self.image_label = QtWidgets.QLabel()
        self.set_image('imgs/2022-08-05-16-32-54_3.jpg')






        self.current_info_textedit = QtWidgets.QTextEdit("")
        self.current_info_textedit.setStyleSheet("border: 1px solid black;")
        self.current_info_textedit.setFixedHeight(100)

        monitoring_groupbox = QtWidgets.QGroupBox("监测窗口")
        monitoring_layout = QtWidgets.QVBoxLayout()
        monitoring_layout.addWidget(self.image_label)
        # monitoring_layout.addWidget(self.current_info_textedit)
        monitoring_groupbox.setLayout(monitoring_layout)

        monitoring_groupbox2 = QtWidgets.QGroupBox("当前过鱼信息")
        monitoring_layout2 = QtWidgets.QVBoxLayout()
        # monitoring_layout2.addWidget(self.image_label)
        monitoring_layout2.addWidget(self.current_info_textedit)
        monitoring_groupbox2.setLayout(monitoring_layout2)


        monitoring_groupbox_right = QtWidgets.QGroupBox("")
        monitoring_layout_right = QtWidgets.QVBoxLayout()
        monitoring_layout_right.addWidget(monitoring_groupbox)
        monitoring_layout_right.addWidget(monitoring_groupbox2)
        monitoring_groupbox_right.setLayout(monitoring_layout_right)

        splitter_right= QtWidgets.QSplitter(QtCore.Qt.Vertical)
        splitter_right.addWidget(monitoring_groupbox)
        splitter_right.addWidget(monitoring_groupbox2)
        splitter_right.setSizes([self.height()*4//5, self.height()*1//5])


        # 使用splitter将左右两个部分分割
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(monitoring_groupbox_left)
        splitter.addWidget(splitter_right)

        # 设置左侧按钮部分的大小
        splitter.setSizes([self.width() // 5, self.width() * 4 // 5])

        self.setCentralWidget(splitter)

    def create_button(self, text, on_click):
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(on_click)
        self.button_layout.addWidget(button)

    def select_video_path(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "选择视频文件路径")[0]
        if path:
            print("Selected video path:", path)

    def select_fine_model(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, "选择细粒度检测模型权重文件")[0]
        if path:
            print("Selected fine model path:", path)

    def select_coarse_model(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, "选择粗粒度检测模型权重文件")[0]
        if path:
            print("Selected coarse model path:", path)

    def select_tracking_model(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, "选择目标追踪模型权重文件")[0]
        if path:
            print("Selected tracking model path:", path)

    def show_parameter_settings(self):
        parameter_settings_window = ParameterSettingsWindow()
        if parameter_settings_window.exec_() == QtWidgets.QDialog.Accepted:
            iou_threshold = parameter_settings_window.iou_spinbox.value()
            confidence_threshold = parameter_settings_window.confidence_spinbox.value()
            print("IoU Threshold:", iou_threshold)
            print("Confidence Threshold:", confidence_threshold)

    def start_detection(self):
        print("Starting detection...")

    def set_image(self, path):
        pixmap = QtGui.QPixmap(path)
        self.image_label.setPixmap(pixmap)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
