# Predicting University Graduation Rates

## **Objective:**
Build a regression model to predict university graduation rates for 4-year public and private colleges in the US.

## **Approach:**
Speed dating data is cleaned and aggregated into two data frames to build two separate classification models. The first model predicts whether a round of speed dating will end in a match. The features used in this model were related to how participants scored their dates based on characteristics like attractiveness, intelligence, and ambition. A feature was engineered that measured how in-sync the date was by finding the absolute value of the sum of the differences in how a participant rated their date and how the date rated the participant on each characteristic.  The second model predicts whether a match in a speed dating round results in a date after the speed dating event. The features used in this model were related to how each participant rated their interests in various categories, how much they go out (in general and on dates), and how they view themselves. Numerous features were engineered in order to categorize each activity.

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
