from matplotlib import rcParams
from seaborn import heatmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt


# 创建一个继承自FigureCanvasQTAgg的类
# 也就是一个 QWidget 的子类
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # 一定要把Figure对象作为参数传递进去
        super().__init__(fig)


class Pearson:

    def __init__(self):
        self._sc = None
        self._data = None

    def data_init(self, data):
        pearson_name = data.columns.values.tolist()
        for i in range(len(pearson_name)):
            str_name = pearson_name[i].split('$')
            pearson_name[i] = "".join(str_name[:-1])
            if len(str_name) == 1:
                pearson_name[i] += str_name[-1]
            else:
                pearson_name[i] += "$" + str_name[-1] + "$"
        data.columns = pearson_name
        self._data = data.iloc[:, 1:]

    def heatmap_chart(self, data, color, num, afontsize, cfontsize, isInit, **kwargs):
        if data is None:
            return
        if isInit is False:
            self.data_init(data)
        else:
            self._data = data.iloc[:, 1:]

        rcParams['font.sans-serif'] = ['SimHei']
        rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题,或者转换负号为字符串
        self._sc = MplCanvas(self, width=5, height=4, dpi=100)
        group = self._data.shape[1] // num
        if self._data.shape[1] % num != 0:
            group += 1
        for i in range(group):
            plt.figure()
            if i == group-1:
                heatmap(self._data.iloc[:, i*num:].corr(),
                        annot=True, fmt='.2f', cmap=color, annot_kws={"fontsize": cfontsize})
            else:
                heatmap(self._data.iloc[:, i*num:i*num+num].corr(),
                        annot=True, fmt='.2f', cmap=color, annot_kws={"fontsize": cfontsize})
            plt.xticks(fontsize=afontsize)
            plt.yticks(fontsize=afontsize)
            cax = plt.gcf().axes[-1]
            cax.tick_params(labelsize=afontsize)
        plt.show()