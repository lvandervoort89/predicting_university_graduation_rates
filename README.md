# Predicting University Graduation Rates

## **Objective:**
Build a regression model to predict university graduation rates for 4-year public and private colleges in the US.

## **Approach:**
The features used in the model were the number of students who are part time, out-of-station tuition, as  the percent of applicants admitted, the GPA of applicants, the median ACT composite score of applicants, the percent of Pell Grant recipients among freshmen, and the first-year retention rate.  Additionally, feature engineering was done to add a multiplicative interaction term between the median ACT composite score and whether a university requires standardized test scores.  The training data was evaluated on linear regression, ridge regression, and LASSO regression models, both with the features as is and standard scaled, in order to optimize for R2 and MSE.

## **Featured Techniques:**
- BeautifulSoup web scraping
- Feature Engineering & Selection
- Supervised Machine Learning
- Linear regression
- Regularization
- LASSO
- Ridge regression

## **Data:**
Data from more than 1,000 4-year public and private universities in the US was scraped from [College Results Online.](http://www.collegeresults.org)

## **Results Summary:**
A simple linear regression model with standard scaling of features was selected.  Features included in the final model are number of percent of applicants admitted, out-state tuition, average GPA of applicants, percent of part-time students, median ACT composite scores of applicants, percentage of first-year students with Pell grants, the freshman retention rate, and whether admissions testing was required. The features were used to predict 5-year graduation rates. The model was optimized for R2 and mean square error. On the test data, the model had a R2 of 0.74 and MSE of 112.4.
