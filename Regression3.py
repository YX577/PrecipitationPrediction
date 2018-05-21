import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from netCDF4 import Dataset
import itertools as it
from sklearn import svm
from sklearn.model_selection import cross_val_score
import matplotlib as mpl
from matplotlib.pyplot import cm
from sklearn import preprocessing, cross_validation
import math
from sklearn.model_selection import cross_val_score

def preparingData(q, p):
    # reading netcdf
    netcdf_entire_dataset = Dataset("F:/dataset/entire_dataset.nc", "r")
    rain_models = netcdf_entire_dataset.variables['rain_models']
    days_error_rate_file = netcdf_entire_dataset.variables['days'][:]
    time_error_rate_file = netcdf_entire_dataset.variables['time'][:]
    models_error_rate_file = netcdf_entire_dataset.variables['models'][:]

    size = 24*10
    total_dataset = np.empty(shape=(25,size))

    for i in range(25):
        # print(i)
        x = []
        for j in range(24):
            # print(j)
            for k in range(10):
                print(i, j, k)
                data = rain_models[j,k,i,q,p]
                # if data < 5: data = 0
                x.append(data)
                # x.append(list(it.chain.from_iterable(data)))  # flatten the list
        total_dataset[i-7] = x #list(it.chain.from_iterable(x))
            # print(total_dataset[i])
        # print(total_dataset)
        # print(total_dataset.transpose().shape)

    col_mean = np.nanmean(total_dataset, axis=0)
    # Find indicies that you need to replace
    inds = np.where(np.isnan(total_dataset))
    # Place column means in the indices. Align the arrays using take
    total_dataset[inds] = np.take(col_mean, inds[1])

    return total_dataset.transpose()

# preparingData()

def load_data(td):
    # td.reshape(250000, 5)
    # X = td[:, 1:]
    # y = td[:,0]
    # forecast_out = int(math.ceil(0.20 * len(td)))

    # Train = td[:-forecast_out,:]
    # Test = td[-forecast_out:,:]
    Train, Test = train_test_split(td, test_size=0.2)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # print(X_train.shape, y_train.shape)
    # print(X_test.shape, y_test.shape)
    return Train, Test


def linearRegression(td):
    Train, Test = load_data(td)
    X_train, X_test, y_train, y_test = train_test_split(Train[:, 1:], Train[:,0], test_size=0.2)
    clf = LinearRegression(n_jobs=-1)
    # print(clf.coef_)
    clf.fit(X_train, y_train)
    print(clf.coef_)
    confidence = clf.score(X_test, y_test)
    print(confidence)
    print(clf.coef_)
    # scores = cross_val_score(clf, Train[:, 1:], Train[:,0], cv=5)
    # print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    # plot_result(0, 1)
    #
    predictedValue = clf.predict(Test[:, 1:])
    plot_result(predictedValue, Test[:,0])

def plot_result(predictedValue, OriginalValue):
    mpl.style.use('seaborn')
    # color = iter(cm.rainbow(np.linspace(0, 1, len(X_train[0]))))

    plt.plot(OriginalValue, color='Green', label='Actual')
    plt.plot(predictedValue, color='Red', label='New Prediction')
    plt.legend()
    # for i in range(len(X_train[0])):
    #     c = next(color)
    #     plt.plot(X_train[:,i], c=c, label='Old Prediction'+str(i))



    plt.show()


for q in range(360, 1155):
    for p in range(700, 1683):
        td = preparingData(q, p)
        linearRegression(td)

# obj = LinearRegressionClass;
# df = obj.readFromDB(obj, ma=[50, 100, 200])
# obj.load_data(obj, df)