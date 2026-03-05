# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QTabWidget,
    QTextEdit, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(1048, 600)
        self.tabWidget = QTabWidget(Widget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 0, 1051, 691))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.label_4 = QLabel(self.tab)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(20, 190, 151, 31))
        self.simulate_button = QPushButton(self.tab)
        self.simulate_button.setObjectName(u"simulate_button")
        self.simulate_button.setGeometry(QRect(20, 380, 211, 51))
        self.damping_checkbox = QCheckBox(self.tab)
        self.damping_checkbox.setObjectName(u"damping_checkbox")
        self.damping_checkbox.setGeometry(QRect(20, 310, 191, 31))
        self.error_compare_checkbox = QCheckBox(self.tab)
        self.error_compare_checkbox.setObjectName(u"error_compare_checkbox")
        self.error_compare_checkbox.setGeometry(QRect(20, 260, 191, 31))
        self.label_5 = QLabel(self.tab)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(20, 130, 151, 31))
        self.angle_plot_widget = QWidget(self.tab)
        self.angle_plot_widget.setObjectName(u"angle_plot_widget")
        self.angle_plot_widget.setGeometry(QRect(509, 0, 511, 281))
        self.energy_plot_widget = QWidget(self.tab)
        self.energy_plot_widget.setObjectName(u"energy_plot_widget")
        self.energy_plot_widget.setGeometry(QRect(510, 300, 511, 261))
        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 70, 151, 31))
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 10, 151, 31))
        self.time_input = QLineEdit(self.tab)
        self.time_input.setObjectName(u"time_input")
        self.time_input.setGeometry(QRect(200, 190, 241, 31))
        self.omega_input = QLineEdit(self.tab)
        self.omega_input.setObjectName(u"omega_input")
        self.omega_input.setGeometry(QRect(200, 130, 241, 31))
        self.optimal_length_result_label = QLabel(self.tab)
        self.optimal_length_result_label.setObjectName(u"optimal_length_result_label")
        self.optimal_length_result_label.setGeometry(QRect(260, 310, 201, 31))
        self.angle_input = QLineEdit(self.tab)
        self.angle_input.setObjectName(u"angle_input")
        self.angle_input.setGeometry(QRect(200, 70, 241, 31))
        self.length_input = QLineEdit(self.tab)
        self.length_input.setObjectName(u"length_input")
        self.length_input.setGeometry(QRect(200, 10, 241, 31))
        self.find_optimal_length_button = QPushButton(self.tab)
        self.find_optimal_length_button.setObjectName(u"find_optimal_length_button")
        self.find_optimal_length_button.setGeometry(QRect(250, 380, 211, 51))
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.toolbox_output = QTextEdit(self.tab_2)
        self.toolbox_output.setObjectName(u"toolbox_output")
        self.toolbox_output.setGeometry(QRect(580, 10, 451, 221))
        self.func_input = QLineEdit(self.tab_2)
        self.func_input.setObjectName(u"func_input")
        self.func_input.setGeometry(QRect(160, 110, 311, 31))
        self.param1_input = QLineEdit(self.tab_2)
        self.param1_input.setObjectName(u"param1_input")
        self.param1_input.setGeometry(QRect(160, 180, 311, 31))
        self.param2_input = QLineEdit(self.tab_2)
        self.param2_input.setObjectName(u"param2_input")
        self.param2_input.setGeometry(QRect(160, 250, 311, 31))
        self.param1_label = QLabel(self.tab_2)
        self.param1_label.setObjectName(u"param1_label")
        self.param1_label.setGeometry(QRect(20, 180, 141, 31))
        self.param2_label = QLabel(self.tab_2)
        self.param2_label.setObjectName(u"param2_label")
        self.param2_label.setGeometry(QRect(20, 250, 141, 31))
        self.method_select = QComboBox(self.tab_2)
        self.method_select.setObjectName(u"method_select")
        self.method_select.setGeometry(QRect(170, 20, 251, 41))
        self.run_method_button = QPushButton(self.tab_2)
        self.run_method_button.setObjectName(u"run_method_button")
        self.run_method_button.setGeometry(QRect(210, 350, 191, 71))
        self.param1_label_2 = QLabel(self.tab_2)
        self.param1_label_2.setObjectName(u"param1_label_2")
        self.param1_label_2.setGeometry(QRect(20, 110, 141, 31))
        self.convergence_plot_widget = QWidget(self.tab_2)
        self.convergence_plot_widget.setObjectName(u"convergence_plot_widget")
        self.convergence_plot_widget.setGeometry(QRect(580, 240, 451, 321))
        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(Widget)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.label_4.setText(QCoreApplication.translate("Widget", u"Max Time (s):", None))
        self.simulate_button.setText(QCoreApplication.translate("Widget", u"Simulate", None))
        self.damping_checkbox.setText(QCoreApplication.translate("Widget", u"Include Damping", None))
        self.error_compare_checkbox.setText(QCoreApplication.translate("Widget", u"Show Error Comparison", None))
        self.label_5.setText(QCoreApplication.translate("Widget", u"Initial Velocity:", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"Initial Angle (\u00b0):", None))
        self.label.setText(QCoreApplication.translate("Widget", u"Lenght (m):", None))
        self.optimal_length_result_label.setText("")
        self.find_optimal_length_button.setText(QCoreApplication.translate("Widget", u"Find Optimal Length", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Widget", u"Pendulum", None))
        self.param1_label.setText(QCoreApplication.translate("Widget", u"Parameter 1:", None))
        self.param2_label.setText(QCoreApplication.translate("Widget", u"Parameter 2:", None))
        self.run_method_button.setText(QCoreApplication.translate("Widget", u"Solve", None))
        self.param1_label_2.setText(QCoreApplication.translate("Widget", u"Function f(x):", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Widget", u"Toolbox", None))
    # retranslateUi

