import sd
import os
import glob

try:
    from .PIL_11_1 import Image
except:
    try:
        from .PIL_11_2 import Image
    except:
        from PIL import Image

# from PIL import Image

from sd.api import sdproperty
try:
    from PySide2 import QtWidgets, QtCore, QtGui
    PYSIDE_VERSION = 2
except:
    from PySide6 import QtWidgets, QtCore, QtGui
    PYSIDE_VERSION = 6

from sd.api.apiexception import APIException



BASE_STYLE_SHEET = """
/* 全局基础样式 */
QWidget {
    background-color: #353535;
    color: #d0d0d0;
    font-family: "Segoe UI", Arial;
    font-size: 12px;
    selection-background-color: #4070a0;
    selection-color: white;
}

/* 主窗口 */
QMainWindow {
    background-color: #2d2d2d;
}

/* 按钮 */
QPushButton {
    background-color: #404040;
    border: 1px solid #505050;
    border-radius: 3px;
    padding: 5px 12px;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #4a4a4a;
    border-color: #606060;
}

QPushButton:pressed {
    background-color: #303030;
    border-color: #404040;
}

QPushButton:disabled {
    color: #707070;
    background-color: #353535;
}

/* 输入框 */
QLineEdit, QTextEdit {
    background-color: #2d2d2d;
    border: 1px solid #505050;
    border-radius: 3px;
    padding: 4px;
    selection-background-color: #4070a0;
}

QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #6080b0;
}

/* 下拉框 */
QComboBox {
    background-color: #404040;
    border: 1px solid #505050;
    border-radius: 3px;
    padding: 4px 20px 4px 8px;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-left: 1px solid #505050;
}

QComboBox::down-arrow {
    image: url(icons/down_arrow.svg);
    width: 12px;
    height: 12px;
}

QComboBox QAbstractItemView {
    background-color: #404040;
    border: 1px solid #505050;
    selection-background-color: #4070a0;
}

/* 滑动条 */
QSlider::groove:horizontal {
    background: #404040;
    height: 4px;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    background: #606060;
    border: 1px solid #505050;
    width: 14px;
    margin: -6px 0;
    border-radius: 7px;
}

QSlider::handle:horizontal:hover {
    background: #707070;
}

/* 复选框/单选框 */
QCheckBox, QRadioButton {
    spacing: 6px;
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 16px;
    height: 16px;
}

QCheckBox::indicator {
    image: url(icons/checkbox_unchecked.svg);
}

QCheckBox::indicator:checked {
    image: url(icons/checkbox_checked.svg);
}

QRadioButton::indicator {
    image: url(icons/radio_unchecked.svg);
}

QRadioButton::indicator:checked {
    image: url(icons/radio_checked.svg);
}

/* 分组框 */
QGroupBox {
    border: 1px solid #505050;
    border-radius: 3px;
    margin-top: 1ex;
    padding-top: 12px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 3px;
}

/* 标签页 */
QTabWidget::pane {
    border: 1px solid #505050;
    top: -1px;
}

QTabBar::tab {
    background: #404040;
    border: 1px solid #505050;
    border-bottom: none;
    padding: 6px 12px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background: #2d2d2d;
    border-color: #505050;
}

QTabBar::tab:hover {
    background: #4a4a4a;
}

/* 进度条 */
QProgressBar {
    border: 1px solid #505050;
    border-radius: 3px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #4070a0;
    width: 10px;
}

/* ------------------- QListWidget 主容器 ------------------- */
QListWidget {
    background-color: #2d2d2d;        /* 列表背景色 */
    border: 1px solid #505050;        /* 边框颜色 */
    border-radius: 3px;               /* 圆角半径 */
    padding: 2px;                     /* 内边距 */
    outline: none;                    /* 移除焦点虚线框 */
}

/* ------------------- 列表项样式 ------------------- */
QListWidget::item {
    color: #d0d0d0;                   /* 文字颜色 */
    height: 22px;                     /* 项高度 */
    padding: 2px 4px;                 /* 文字内边距 */
    border-radius: 2px;               /* 项圆角 */
    margin: 1px 3px;                  /* 项外边距 */
}

/* 鼠标悬停效果 */
QListWidget::item:hover {
    background-color: #3a3a3a;        /* 悬停背景色 */
}

/* 选中状态 */
QListWidget::item:selected {
    background-color: #3a3a3a;        /* Substance 标志蓝 */
    color: white;
}

/* 选中未聚焦状态 */
QListWidget::item:selected:!active {
    background-color: #405060;        /* 较暗的选中色 */
}

/* 禁用状态 */
QListWidget::item:disabled {
    color: #707070;
}

/* ------------------- 滚动条样式 ------------------- */
QScrollBar:vertical {
    background: #353535;              /* 滚动条背景 */
    width: 12px;                      /* 垂直滚动条宽度 */
    margin: 2px 0;
}

QScrollBar::handle:vertical {
    background: #505050;              /* 滑块颜色 */
    min-height: 20px;                 /* 最小滑块高度 */
    border-radius: 6px;
}

QScrollBar::handle:vertical:hover {
    background: #606060;              /* 悬停颜色 */
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    background: none;                 /* 移除上下箭头区域 */
    border: none;
    height: 0;
}

QScrollBar:horizontal {               /* 水平滚动条同理 */
    background: #353535;
    height: 12px;
    margin: 0 2px;
}

QScrollBar::handle:horizontal {
    background: #505050;
    min-width: 20px;
    border-radius: 6px;
}

/* ------------------- 角部样式 ------------------- */
QScrollBar::corner {
    background: #2d2d2d;              /* 滚动条角落颜色 */
}
"""


#
def export_texture(node, output_dir, index, ext='jpg'):
    # 现在只限制为第一个output的图片
    outputProperty = node.getProperties(sdproperty.SDPropertyCategory.Output)[0]

    # Get the property value
    propertyValue = node.getPropertyValue(outputProperty)

    # Get the property value as texture
    propertyTexture = propertyValue.get()

    # Save the texture on disk

    fileName = 'output_' + str(index) + '.' + str(ext)
    textureFileName = os.path.abspath(os.path.join(output_dir, fileName))

    try:
        propertyTexture.save(textureFileName)
    except APIException:
        print('Fail to save texture %s' % textureFileName)


def get_preview_tex(node):
    nodeDefinition = node.getDefinition()

    # 现在只限制为第一个output的图片
    outputProperty = nodeDefinition.getProperties(sdproperty.SDPropertyCategory.Output)[0]

    # Get the property value
    propertyValue = node.getPropertyValue(outputProperty)

    # Get the property value as texture
    propertyTexture = propertyValue.get()

    return propertyTexture


def show_info(uiMgr, message = "操作已完成!"):
    # 获取 Substance Designer 的主窗口作为父级（确保对话框居中）
    parent = uiMgr.getMainWindow()

    QtWidgets.QMessageBox.information(
        parent,  # 父窗口
        "提示",  # 标题
        message  # 内容
    )

def show_warning(uiMgr, message = "警告警告警告!"):
    parent = uiMgr.getMainWindow()
    QtWidgets.QMessageBox.warning(
        parent,
        "警告",
        message
    )

def show_error(uiMgr, message = "寄!"):
    parent = uiMgr.getMainWindow()
    QtWidgets.QMessageBox.critical(
        parent,
        "错误",
        message
    )


class MyProcessUI(QtWidgets.QMainWindow):
    _current_instance = None

    def __init__(self, uiMgr):
        super(MyProcessUI, self).__init__(parent=uiMgr.getMainWindow())

        self.uiMgr = uiMgr

        self.setMinimumSize(400, 300)
        self.setMaximumHeight(300)
        # self.setToolTip()
        self.setWindowTitle("Process Texture Tools  (｡˘•ε•˘｡) ")

        self.create_widge()
        self.create_layout()

        self.setStyleSheet(BASE_STYLE_SHEET)

        self.process_node_list = []

    def create_widge(self):
        self.editor_output_dir = QtWidgets.QLineEdit()
        base_path = os.path.dirname(
            sd.getContext().getSDApplication().getPackageMgr().getUserPackages()[0].getFilePath()
        )
        self.editor_output_dir.setText(base_path)

        self.btn_get_dir = QtWidgets.QPushButton()
        self.btn_get_dir.setText("Select Folder")
        self.btn_get_dir.clicked.connect(self.get_output_dir)
        self.btn_get_dir.setToolTip("当然就只是选择文件夹咯(it's just about selecting folders.)")

        self.label_duration = QtWidgets.QLabel("Duration:")
        self.label_duration.setToolTip("每一帧的间隔（The interval between each frame）")
        self.label_duration.setMinimumWidth(50)

        self.slider_duration = QtWidgets.QSlider(orientation=QtCore.Qt.Horizontal)
        self.slider_duration.setMinimumWidth(200)
        self.slider_duration.setRange(0, 30)
        self.slider_duration.setValue(10)
        self.slider_duration.valueChanged.connect(self.slider_changed)

        self.editor_duration = QtWidgets.QLineEdit()
        self.editor_duration.setMaximumWidth(50)
        self.editor_duration.setValidator(QtGui.QDoubleValidator(0.0, 3.0, 1))
        self.editor_duration.editingFinished.connect(self.lineedit_changed)

        self.slider_changed(self.slider_duration.value())

        self.btn_get_select = QtWidgets.QPushButton()
        self.btn_get_select.setMinimumSize(60, 40)
        self.btn_get_select.setText("Get Select")
        self.btn_get_select.setToolTip("将选择的节点加入列表(Add the selected nodes to the list)")
        self.btn_get_select.clicked.connect(self.get_select_node)

        self.btn_export_tex = QtWidgets.QPushButton()
        self.btn_export_tex.setMinimumSize(60, 40)
        self.btn_export_tex.setText("Export Tex")
        self.btn_export_tex.setToolTip("将列表导出图片与Gif(Export the list as images and Gif animations)")
        self.btn_export_tex.clicked.connect(self.export_process_gif)


        self.list_node = QtWidgets.QListWidget()
        self.list_node.setFlow(QtWidgets.QListView.Flow.LeftToRight)
        self.list_node.setMovement(QtWidgets.QListView.Movement.Snap)
        self.list_node.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.InternalMove)
        self.list_node.setWrapping(False)
        self.list_node.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.list_node.setGridSize(QtCore.QSize(120, 120))
        self.list_node.setIconSize(QtCore.QSize(100, 120))
        self.list_node.setFixedHeight(140)

        self.list_node.model().rowsMoved.connect(self.order_queue)
        self.list_node.itemDoubleClicked.connect(self.delete_item)

    def create_layout(self):
        output_h_layout = QtWidgets.QHBoxLayout()
        output_h_layout.addWidget(self.editor_output_dir)
        output_h_layout.addWidget(self.btn_get_dir)

        select_h_layout = QtWidgets.QHBoxLayout()
        select_h_layout.addWidget(self.btn_get_select)
        select_h_layout.addWidget(self.btn_export_tex)

        duration_h_layout = QtWidgets.QHBoxLayout()
        duration_h_layout.addWidget(self.label_duration)
        duration_h_layout.addWidget(self.slider_duration)
        duration_h_layout.addWidget(self.editor_duration)

        global_v_layout = QtWidgets.QVBoxLayout()
        global_v_layout.addLayout(output_h_layout)
        global_v_layout.addLayout(select_h_layout)
        global_v_layout.addLayout(duration_h_layout)
        global_v_layout.addWidget(self.list_node)

        center_widget = QtWidgets.QWidget()
        center_widget.setLayout(global_v_layout)

        self.setCentralWidget(center_widget)

    @classmethod
    def create_new(cls, uiMgr):
        if cls._current_instance:
            cls._current_instance.close()
            # pyside6才有
            # cls._current_instance.deteleLater()

        cls._current_instance = MyProcessUI(uiMgr)
        cls._current_instance.show()

    def get_output_dir(self):
        floder_path = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "选择导出的文件夹",
            self.editor_output_dir.text(),
            QtWidgets.QFileDialog.ShowDirsOnly
        )

        if floder_path:
            self.editor_output_dir.setText(floder_path)

    def get_select_node(self):
        nodes = self.uiMgr.getCurrentGraphSelectedNodes()

        for node in nodes:
            preview_tex = get_preview_tex(node)
            preview_image = self.uiMgr.convertSDTextureToQImage(preview_tex)
            preview_map = QtGui.QPixmap(preview_image)
            preview_icon = QtGui.QIcon(preview_map)

            item = QtWidgets.QListWidgetItem()
            item.setIcon(preview_icon)

            self.process_node_list.append(node)

            self.list_node.addItem(item)


    def order_queue(self, parent, start, end, destination, row):
        """根据拖动操作实时调整外部列表顺序"""
        # 计算移动的元素数量
        count = end - start + 1
        moved_elements = self.process_node_list[start:end+1]

        # 删除原位置的元素
        del self.process_node_list[start:end+1]

        # 计算插入位置（考虑拖动方向）
        insert_pos = row - count if row > start else row

        # 插入到新位置
        self.process_node_list[insert_pos:insert_pos] = moved_elements

        print(self.process_node_list)


    def export_process_gif(self):

        gif_output_dir = self.editor_output_dir.text()
        tex_output_dir = os.path.normpath(gif_output_dir + "/PrecessTex")

        tex_files = glob.glob(os.path.join(tex_output_dir, "*"))
        for file in tex_files:
            os.remove(file)


        # 先导出图片
        for index in range(len(self.process_node_list)):
            export_texture(self.process_node_list[index],
                           tex_output_dir,
                           index,)

        # 导出为Gif
        tex_files = sorted(glob.glob(os.path.join(tex_output_dir, "*.jpg")))
        frames = []
        for file in tex_files:
            img = Image.open(file)
            frames.append(img)

        output_gif = os.path.join(gif_output_dir, "process.gif")
        duration = self.slider_duration.value() * 100

        frames[0].save(
            output_gif,
            format="GIF",
            append_images=frames[1:],
            save_all=True,
            duration=duration,
            loop=0,
            optimize=True,
            disposal=2
        )

        show_info(self.uiMgr, "导出完成")
        os.startfile(gif_output_dir)

    # 删除Item和对应列表的节点
    def delete_item(self, item):
        item_index = self.list_node.indexFromItem(item).row()
        del self.process_node_list[item_index]

        self.list_node.takeItem(item_index)

    def slider_changed(self, value):
        float_value = value / 10.0
        self.editor_duration.setText(f"{float_value:.1f}")

    def lineedit_changed(self):
        text = self.editor_duration.text()
        try:
            value = float(text)
            if 0.0 <= value <= 20.0:
                slider_value = int(round(value * 10))
                with QtCore.QSignalBlocker(self.slider_duration):
                    self.slider_duration.setValue(slider_value)
            else:
                self.slider_changed(self.slider_duration.value())  # 恢复原值
        except ValueError:
            self.slider_changed(self.slider_duration.value())  # 输入无效时恢复



def create_process_ui(uiMgr):
    ui = MyProcessUI.create_new(uiMgr)


menu_id = "weilai.tools.process_tex"
app = sd.getContext().getSDApplication()
uiMgr = app.getQtForPythonUIMgr()

def create_process_menu():


    nemu = uiMgr.findMenuFromObjectName(menu_id)
    if nemu is not None:
        uiMgr.deleteMenu(menu_id)

    menu = uiMgr.newMenu(menuTitle="Tools", objectName="weilai.tools.process_tex")

    if PYSIDE_VERSION == 2:
        act = QtWidgets.QAction("Process Tex", menu)
    else:
        act = QtGui.QAction("Process Tex", menu)

    act.triggered.connect(lambda: create_process_ui(uiMgr))

    menu.addAction(act)
# create_process_menu()

def delete_process_menu():
    nemu = uiMgr.findMenuFromObjectName(menu_id)
    if nemu is not None:
        uiMgr.deleteMenu(menu_id)