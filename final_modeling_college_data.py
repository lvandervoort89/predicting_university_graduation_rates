'''
This scripts loads the date_data and uses a Linear Regression model with standard scaling
to predict university graduation rates.
'''
import pickle
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def separate_features_and_target(dataframe):
    '''
    Returns 2 dataframes where features contains only the features for the
    model and target contains the targets.
    '''

    features_grad_rate = dataframe.drop('five_year_grad_rate', axis=1)
    target_grad_rate = dataframe['five_year_grad_rate']

    return features_grad_rate, target_grad_rate

def train_test_split_data(five_college_df):
    '''
    Return train and test dataframes.
    '''

    feature_grad_rate, target_grad_rate = separate_features_and_target(five_college_df)

    x_train, x_test, y_train, y_test = train_test_split(feature_grad_rate, target_grad_rate,
                                                        test_size=.2)

    return x_train, x_test, y_train, y_test

def final_linear_regression_model_with_scaling(x_train, x_test, y_train, y_test):
    '''
    Takes in a dataframe and calls other functions to split the data into train and test sets.
    Models data using a linear regression model with standard scaling to predict university
    graduation rates. Prints train and test r2 and mse. Pickles the model for future use.
    '''
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train.values)
    x_test_scaled = scaler.transform(x_test.values)

    linear_regression = LinearRegression()
    linear_regression.fit(x_train_scaled, y_train)
    y_pred = linear_regression.predict(x_test_scaled)

    r2_train = linear_regression.score(x_train_scaled, y_train)
    r2_test = linear_regression.score(x_test_scaled, y_test)
    mse = mean_squared_error(y_test, y_pred)

    # Print model results
    print('Linear Regression Results with Scaling:\n'
          f'R^2 Train: {r2_train},\n'
          f'R^2 Test: {r2_test},\n'
          f'MSE: {mse}')

    # Pickle model
    with open('linear_regression.pkl', 'wb') as f:
        pickle.dump(linear_regression, f)

def main():
    '''
    Loads in the date_data, separates the features and target, separates the data
    into train-test-split, and uses a Linear Regression model with standard scaling.
    Prints the results and pickles the model.
    '''

    # Load in data
    five_college_df = pd.read_csv('five_college_df.csv')

    # Call internal functions to this script
    x_train, x_test, y_train, y_test = train_test_split_data(five_college_df)
    final_linear_regression_model_with_scaling(x_train, x_test, y_train, y_test)

main()
