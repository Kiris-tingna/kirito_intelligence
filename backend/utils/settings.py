# - * - coding:utf-8  - * - -
'''
@ Author: Tinkle G
'''
import re
import os
import pandas as pd
import json
import collections
import numpy as np
import random
import utils.gentext
import re

import math
from sklearn import preprocessing
from sklearn.svm import SVR
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import  RandomForestRegressor
from sklearn.linear_model import Lasso
from sklearn import metrics


models = {'LR':LinearRegression(),'SVR':SVR(C=3,kernel='rbf'),'GBDT':GradientBoostingRegressor(n_estimators=6),
          'RF':RandomForestRegressor(n_estimators=4),
          'Lasso':Lasso(alpha=0.1)}

metrics_dict = {'r2_score': metrics.r2_score, 'root_mean_squared_error': metrics.mean_squared_error,
                'explained_variance_score': metrics.explained_variance_score}

os_path = '../data/'
