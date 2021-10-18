import pandas as pd


class GrayCorrelation:

    def __init__(self, data):
        if data is not None:
            data.dropna(inplace=True, how='all')  # 删除全为空值的行
        self._df = data

    def gray_analysis(self, rho, acc):  # 默认系数为0.5
        if self._df is None:
            return None
        std_data = self._df.iloc[:, 1:].T
        std_data_mean = std_data.mean(axis=1)  # 求均值
        std_data_std = std_data.std(axis=1)  # 求标准差
        # 标准化处理
        for i in range(std_data.index.size):
            std_data.iloc[i, :] = (std_data.iloc[i, :] - std_data_mean[i]) / std_data_std[i]
        # 因素数据与参考数据求差
        factor_data = pd.DataFrame()
        for i in range(std_data.index.size - 1):
            temp = pd.Series(std_data.iloc[i, :] - std_data.iloc[-1, :])
            factor_data = factor_data.append(temp, ignore_index=True)
        # 获取表中最大值与最小值
        mmax = factor_data.abs().max().max()
        mmin = factor_data.abs().min().min()
        # 计算关联度
        ksi = ((mmin + rho * mmax) / (abs(factor_data) + rho * mmax))
        result = pd.DataFrame(columns=std_data.iloc[:-1, :].index.values.tolist(), index=[str(round(rho, 1))+'结果'])
        for i in range(ksi.index.size):
            result.iloc[0][i] = round(ksi.iloc[i, :].sum() / sum(ksi.iloc[i, :].isnull() == False), acc)
        return result

