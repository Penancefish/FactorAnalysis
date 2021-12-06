from itertools import combinations
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
import pandas as pd
from Lib.analysis import GrayCorrelation


class Regression:
    def __init__(self):
        self._table = None
        self._anaValue = None
        self._pearValue = None

    def main_program(self, data, para_num, accu, rho=0.1, **kwargs):
        if data is None:
            return None
        # 计算得到灰色关联结果及皮尔逊结果
        self._anaValue = GrayCorrelation(data).gray_analysis(rho, 6)
        self._pearValue = data.iloc[:, 1:].corr().iloc[:-1, -1]
        para_num = min(para_num, self._pearValue.index.size)
        # 存储参考因素和比较因素，并根据皮尔逊结果，将需要列*-1，然后标准化
        compare_data = data.iloc[:, 1:-1]
        last_data = data.iloc[:, -1].values
        for i in self._pearValue.index:
            if self._pearValue[i] < 0:
                compare_data[i] *= -1
        compare_mean = compare_data.mean()  # 求均值
        compare_std = compare_data.std()  # 求标准差
        for i in range(compare_data.columns.size):
            compare_data.iloc[:, i] = (compare_data.iloc[:, i] - compare_mean[i]) / compare_std[i]
        # 计算组合可能性
        combine_list = []
        for i in combinations(list(compare_data), para_num):
            combine_list.append(list(i))
        # 遍历所有可能性
        combine_num = []
        R2 = []
        valid_num = []
        valid_combine = []
        valid_a = []
        valid_b = []
        valid_w = []
        for i in range(len(combine_list)):
            temp_data = compare_data[combine_list[i]].T
            temp_analysis = self._anaValue[combine_list[i]]
            w = (temp_analysis.iloc[0, :] / sum(temp_analysis.iloc[0, :])).values
            x = w.dot(temp_data)
            valid_value = pd.DataFrame([x, last_data]).dropna(axis=1)
            if valid_value.columns.size < 3:
                continue
            # 记录有效数据
            valid_num.append(valid_value.columns.size)
            valid_combine.append(combine_list[i])
            valid_x = valid_value.iloc[[0], :].T
            valid_y = valid_value.iloc[1, :].values
            # 线性回归
            line = LinearRegression()
            line.fit(valid_x, valid_y)
            a = line.coef_.round(accu)
            b = line.intercept_
            valid_a.append(a)
            valid_b.append(round(b, accu))
            valid_w.append(w)
            # 计算R^2
            pre_values = line.predict(valid_x)
            R2.append(round(r2_score(valid_y, pre_values), accu))
            combine_num.append(para_num)
        if len(R2) == 0:
            return None
        self._table = pd.DataFrame([combine_num, R2, valid_combine, valid_num, valid_a, valid_b, valid_w]).T
        self._table.columns = ['组合数', 'R2', '组合方式', '有效数', 'a', 'b', 'w']
        return self._table

    def get_max_merge(self):
        if self._table is None:
            return None
        max_value = self._table['R2'].max()
        max_result = self._table.loc[self._table['R2'] == max_value]
        return max_result
