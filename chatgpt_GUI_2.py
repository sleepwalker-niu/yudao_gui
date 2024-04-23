import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import random

class ParameterSettingsWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("参数设置")
        self.setFixedSize(300, 300)

        layout = QtWidgets.QVBoxLayout()

        self.coarse_iou_label = QtWidgets.QLabel("粗粒度模型IoU阈值：")
        layout.addWidget(self.coarse_iou_label)
        self.coarse_iou_spinbox = QtWidgets.QDoubleSpinBox()
        self.coarse_iou_spinbox.setMinimum(0)
        self.coarse_iou_spinbox.setMaximum(1)
        layout.addWidget(self.coarse_iou_spinbox)

        self.fine_iou_label = QtWidgets.QLabel("细粒度模型IoU阈值：")
        layout.addWidget(self.fine_iou_label)
        self.fine_iou_spinbox = QtWidgets.QDoubleSpinBox()
        self.fine_iou_spinbox.setMinimum(0)
        self.fine_iou_spinbox.setMaximum(1)
        layout.addWidget(self.fine_iou_spinbox)

        self.coarse_confidence_label = QtWidgets.QLabel("粗粒度模型置信度阈值：")
        layout.addWidget(self.coarse_confidence_label)
        self.coarse_confidence_spinbox = QtWidgets.QDoubleSpinBox()
        self.coarse_confidence_spinbox.setMinimum(0)
        self.coarse_confidence_spinbox.setMaximum(1)
        layout.addWidget(self.coarse_confidence_spinbox)

        self.fine_confidence_label = QtWidgets.QLabel("细粒度模型置信度阈值：")
        layout.addWidget(self.fine_confidence_label)
        self.fine_confidence_spinbox = QtWidgets.QDoubleSpinBox()
        self.fine_confidence_spinbox.setMinimum(0)
        self.fine_confidence_spinbox.setMaximum(1)
        layout.addWidget(self.fine_confidence_spinbox)

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

        monitoring_groupbox_upper_left = QtWidgets.QGroupBox("控制区")
        monitoring_layout_left = QtWidgets.QVBoxLayout()
        monitoring_layout_left.addWidget(left_widget)
        monitoring_groupbox_upper_left.setLayout(monitoring_layout_left)
        monitoring_groupbox_upper_left.setFixedSize(250, 650)
        # 创建监测窗口和当前过鱼信息
        self.image_label = QtWidgets.QLabel()
        self.set_image('imgs/2022-08-05-16-32-54_3.jpg')

        self.current_info_layout = QtWidgets.QVBoxLayout()
        self.create_fish_info_group("鱼类上行", self.current_info_layout)
        self.create_fish_info_group("鱼类下行", self.current_info_layout)

        monitoring_groupbox = QtWidgets.QGroupBox("监测窗口")
        monitoring_layout = QtWidgets.QVBoxLayout()
        monitoring_layout.addWidget(self.image_label)
        # monitoring_layout.addWidget(self.current_info_textedit)
        monitoring_groupbox.setLayout(monitoring_layout)
        monitoring_groupbox.setFixedSize(700,650)

        monitoring_groupbox_down = QtWidgets.QGroupBox("当前过鱼信息")
        monitoring_groupbox_down.setLayout(self.current_info_layout)

        splitter_upper = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter_upper.addWidget(monitoring_groupbox_upper_left)
        splitter_upper.addWidget(monitoring_groupbox)
        # splitter_upper.setSizes([250, 600])

        # 使用splitter将左右两个部分分割
        splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(splitter_upper)
        splitter.addWidget(monitoring_groupbox_down)

        # 设置左侧按钮部分的大小
        splitter.setSizes([150, self.width()-150])

        self.setCentralWidget(splitter)

    def create_button(self, text, on_click):
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(on_click)
        self.button_layout.addWidget(button)

    def select_video_path(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "选择视频文件路径")
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
            coarse_iou_threshold = parameter_settings_window.coarse_iou_spinbox.value()
            fine_iou_threshold = parameter_settings_window.fine_iou_spinbox.value()
            coarse_confidence_threshold = parameter_settings_window.coarse_confidence_spinbox.value()
            fine_confidence_threshold = parameter_settings_window.fine_confidence_spinbox.value()
            print("Coarse IoU Threshold:", coarse_iou_threshold)
            print("Fine IoU Threshold:", fine_iou_threshold)
            print("Coarse Confidence Threshold:", coarse_confidence_threshold)
            print("Fine Confidence Threshold:", fine_confidence_threshold)

    def start_detection(self):
        print("Starting detection...")

    def set_image(self, path):
        pixmap = QtGui.QPixmap(path)
        self.image_label.setPixmap(pixmap)

    def create_fish_info_group(self, title, layout):
        groupbox = QtWidgets.QGroupBox(title)
        grid_layout = QtWidgets.QGridLayout()
        fish_species = ["花鲈", "草鱼", "鲫鱼", "罗非鱼", "白甲鱼", "翘嘴", "日本鳗鲡", "鲤鱼", "鲢鳙","未知鱼类"]
        for i, species in enumerate(fish_species):
            label = QtWidgets.QLabel(species)
            label.setAlignment(QtCore.Qt.AlignCenter)  # 居中对齐
            count = 0  # 随机生成当前过鱼数目
            count_edit = QtWidgets.QLineEdit(str(count))
            count_edit.setFixedWidth(30)
            grid_layout.addWidget(label, 0, i)
            grid_layout.addWidget(count_edit, 1, i)
        groupbox.setLayout(grid_layout)
        layout.addWidget(groupbox)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(970, 800)
    window.show()
    sys.exit(app.exec_())
