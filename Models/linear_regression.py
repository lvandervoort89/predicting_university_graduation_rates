'''
This script uses cross-validation to test a Linear Regression model using
training data.
'''
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold

def linear_regression_model_testing(x_data, y_data):
    '''
    A function that models data with a linear regression model using cross-validation
    without scaling.

    Parameters
    ----------
    X : Feature training and validation set.
    y : Target training and validation set.

    Returns
    -------
    Prints the R^2 average of the k-folds for the train and test data, and the
    Mean Square Error of the model.
    '''
    k_folds = KFold(n_splits=5, shuffle=True)

    r2_train, r2_val, mse = [], [], []

    for train_ind, val_ind in k_folds.split(x_data, y_data):
        x_train, y_train = x_data.iloc[train_ind], y_data.iloc[train_ind]
        x_val, y_val = x_data.iloc[val_ind], y_data.iloc[val_ind]

        linear_regression = LinearRegression()
        linear_regression.fit(x_train, y_train)
        y_pred = linear_regression.predict(x_val)

        r2_train.append(linear_regression.score(x_train, y_train))
        r2_val.append(linear_regression.score(x_val, y_val))
        mse.append(mean_squared_error(y_val, y_pred))

    print('Linear regression results:\n'
          f'R^2 Train: {np.mean(r2_train)},\n'
          f'R^2 Train: {np.mean(r2_val)},\n'
          f'MSE: {np.mean(mse)},')
