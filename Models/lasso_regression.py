'''
This script uses cross-validation to test a LASSO Regression model using
training data.
'''
import numpy as np
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold

def lasso_regression_model_testing(x_data, y_data, alpha):
    '''
    A function that models data with a LASSO regression model using cross-validation
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

        lasso_reg = Lasso(alpha=alpha)
        lasso_reg.fit(x_train, y_train)
        y_pred = lasso_reg.predict(x_val)

        r2_train.append(lasso_reg.score(x_train, y_train))
        r2_val.append(lasso_reg.score(x_val, y_val))
        mse.append(mean_squared_error(y_val, y_pred))

    print('LASSO regression results:\n'
          f'R^2 Train: {np.mean(r2_train)},\n'
          f'R^2 Train: {np.mean(r2_val)},\n'
          f'MSE: {np.mean(mse)},')
