import os
import sys

import pandas as pd
from modules.dataP import DHL

path = os.getcwd()
path = os.path.join(path, "assets/Jobcare_data")
# print(path)

data = DHL()
# data = DHL(PATH=path)
# train = pd.read_csv(path + "/train.csv", encoding="utf-8")
# test = pd.read_csv(path + "/test.csv", encoding="utf-8")
# data = DHL(PATH=path, train=train, test=test)
print(data.train.shape)

data.groupby_mean()
print(data.train.shape)

# data.control_params({
#     "drop_column": [],
#     "dummy_column": []
# })
# print(data.f_train.shape)