import pandas as pd
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5 import uic
from Lib.share import SI
from Lib.pandasMod import PandasModel
from Lib.pearson import Pearson
from Lib.analysis import GrayCorrelation
from Lib.regression import Regression


class UIAnalysisWindow:

    def __init__(self):
        SI.analysis_table = pd.DataFrame()
        self.ui = uic.loadUi("analysis.ui")
        self.ui.pushButton.clicked.connect(self.certain)
        self.ui.btn_export.clicked.connect(self.export)

    def certain(self):
        analysis_data = GrayCorrelation(SI.baseTable).gray_analysis(
            self.ui.doubleSpinBox.value(), self.ui.spinBox.value())
        if analysis_data is None:
            return
        else:
            SI.analysis_table = SI.analysis_table.append(analysis_data)
        model = PandasModel(SI.analysis_table)
        self.ui.tableView.setModel(model)

    def export(self):
        openfile_name, _ = QFileDialog.getSaveFileName(self.ui, "选择文件", "", "文件类型(*.xlsx *.xls)")
        if not openfile_name:
            return
        SI.analysis_table.to_excel(openfile_name)


class UIPearsonWindow:

    def __init__(self):
        self.ui = uic.loadUi("pearson.ui")
        color = ["Accent", "Accent_r", "Blues", "Blues_r",
                 "BrBG", "BrBG_r", "BuGn", "BuGn_r", "BuPu",
                 "BuPu_r", "CMRmap", "CMRmap_r", "Dark2", "Dark2_r",
                 "GnBu", "GnBu_r", "Greens", "Greens_r", "Greys",
                 "Greys_r", "OrRd", "OrRd_r", "Oranges", "Oranges_r",
                 "PRGn", "PRGn_r", "Paired", "Paired_r", "Pastel1", "Pastel1_r",
                 "Pastel2", "Pastel2_r", "PiYG", "PiYG_r", "PuBu", "PuBuGn",
                 "PuBuGn_r", "PuBu_r", "PuOr", "PuOr_r", "PuRd", "PuRd_r",
                 "Purples", "Purples_r", "RdBu", "RdBu_r", "RdGy", "RdGy_r",
                 "RdPu", "RdPu_r", "RdYlBu", "RdYlBu_r", "RdYlGn", "RdYlGn_r",
                 "Reds", "Reds_r", "Set1", "Set1_r", "Set2", "Set2_r", "Set3"]
        self.ui.comboBox.addItems(color)
        self.color = self.ui.comboBox.currentText()
        self.ui.comboBox.currentIndexChanged.connect(self.color_changed)
        self.ui.pushButton.clicked.connect(self.certain)

    def certain(self):
        if SI.baseTable is None:
            return
        if SI.baseTable_init is False:
            Pearson().heatmap_chart(SI.baseTable, self.color, self.ui.spinBox.value(),
                                    self.ui.axesFontBox.value(), self.ui.chartFontBox.value(), False)
            SI.baseTable_init = True
        else:
            Pearson().heatmap_chart(SI.baseTable, self.color, self.ui.spinBox.value(),
                                    self.ui.axesFontBox.value(), self.ui.chartFontBox.value(), True)

    def color_changed(self):
        self.color = self.ui.comboBox.currentText()


class UIRegressionWindow:
    def __init__(self):
        self.table1 = None
        SI.regression_table = pd.DataFrame()
        self.ui = uic.loadUi("regression.ui")
        self.ui.btn_regression.clicked.connect(self.regression_analysis)
        self.ui.btn_export_1.clicked.connect(self.export_1)
        self.ui.btn_export_2.clicked.connect(self.export_2)

    def regression_analysis(self):
        if SI.baseTable is None:
            return
        reg = Regression()
        self.table1 = reg.main_program(SI.baseTable, self.ui.spinBox.value(), self.ui.spinBox_2.value())
        model1 = PandasModel(self.table1)
        self.ui.tableView_1.setModel(model1)
        max_value = reg.get_max_merge()
        if max_value is not None:
            SI.regression_table = SI.regression_table.append(max_value)
        model2 = PandasModel(SI.regression_table)
        self.ui.tableView_2.setModel(model2)

    def export_1(self):
        openfile_name, _ = QFileDialog.getSaveFileName(self.ui, "选择文件", "", "文件类型(*.xlsx *.xls)")
        if not openfile_name or self.table1 is None:
            return
        self.table1.to_excel(openfile_name, index=False)

    def export_2(self):
        openfile_name, _ = QFileDialog.getSaveFileName(self.ui, "选择文件", "", "文件类型(*.xlsx *.xls)")
        if not openfile_name:
            return
        SI.regression_table.to_excel(openfile_name, index=False)


class UIMainWindow:

    def __init__(self):
        self._window_ana = None
        self._window_pear = None
        self._window_reg = None
        self.ui = uic.loadUi("main.ui")
        self.ui.actionImport.triggered.connect(self.open_file)
        self.ui.actionAnalysis.triggered.connect(self.open_analysis_window)
        self.ui.actionPearson.triggered.connect(self.open_pearson_window)
        self.ui.actionRegression.triggered.connect(self.open_regression_window)

    def open_file(self):
        openfile_name, _ = QFileDialog.getOpenFileName(self.ui, "选择文件", "", "")
        if not openfile_name:
            return
        SI.baseTable = pd.read_excel(openfile_name)
        model = PandasModel(SI.baseTable)
        self.ui.tableView.setModel(model)

    def open_analysis_window(self):
        self._window_ana = UIAnalysisWindow()
        self._window_ana.ui.show()

    def open_pearson_window(self):
        self._window_pear = UIPearsonWindow()
        self._window_pear.ui.show()

    def open_regression_window(self):
        self._window_reg = UIRegressionWindow()
        self._window_reg.ui.show()


app = QApplication([])
SI.mainWin = UIMainWindow()
SI.mainWin.ui.show()
app.exec_()
