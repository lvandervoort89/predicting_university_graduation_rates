'''
This script uses cross-validation to test a Ridge Regression model using
training data and StandardScaler.
'''
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler

def ridge_regression_model_testing_with_scaling(x_data, y_data, alpha):
    '''
    A function that models data with a ridge regression model using cross-validation
    with scaling.

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

        scaler = StandardScaler()
        x_train_scaled = scaler.fit_transform(x_train.values)
        x_val_scaled = scaler.transform(x_val.values)

        l_ridge = Ridge(alpha=alpha)
        l_ridge.fit(x_train_scaled, y_train)

        r2_train.append(l_ridge.score(x_train_scaled, y_train))
        r2_val.append(l_ridge.score(x_val_scaled, y_val))
        mse.append(mean_squared_error(y_val, l_ridge.predict(x_val_scaled)))

    print('Ridge regression results with scaling:\n'
          f'R^2 Train: {np.mean(r2_train)},\n'
          f'R^2 Train: {np.mean(r2_val)},\n'
          f'MSE: {np.mean(mse)},')
