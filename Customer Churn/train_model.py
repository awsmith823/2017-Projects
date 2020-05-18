import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


FILE_NAME = 'Telco-Customer-Churn.csv'
df = pd.read_csv(FILE_NAME)

# Remove 0 tenure customers
df = df[df['tenure'] > 0].reset_index(drop=True)

# CLEAN DATA USING THE FOLLOWING LAMBDA FUNCTIONS


def inferred_yes_no_lambda(x): return 1 if x == 'Yes' \
    else 0 if x == 'No' \
    else 0 if 'No ' in x \
    else None


column_lambda_funcs = {
    'customerID': lambda x: x,
    'SeniorCitizen': lambda x: x,
    'tenure': lambda x: int(x),
    'MonthlyCharges': lambda x: float(x),
    'TotalCharges': lambda x: float(x),

    'Churn': inferred_yes_no_lambda,
    'Dependents': inferred_yes_no_lambda,
    'DeviceProtection': inferred_yes_no_lambda,
    'MultipleLines': inferred_yes_no_lambda,
    'OnlineSecurity': inferred_yes_no_lambda,
    'OnlineBackup': inferred_yes_no_lambda,
    'PaperlessBilling': inferred_yes_no_lambda,
    'Partner': inferred_yes_no_lambda,
    'PhoneService': inferred_yes_no_lambda,
    'StreamingTV': inferred_yes_no_lambda,
    'StreamingMovies': inferred_yes_no_lambda,
    'TechSupport': inferred_yes_no_lambda,

    'Contract':
        lambda x: {'One year': 1, 'Two year': 1, 'Month-to-month': 0}.get(x),
    'gender':
    lambda x: {'Female': 1, 'Male': 0}.get(x),
    'InternetService':
        lambda x: {'DSL': 1, 'Fiber optic': 1, 'No': 0}.get(x),
    'PaymentMethod':
        lambda x: {'Bank transfer (automatic)': 1,
                   'Credit card (automatic)': 1,
                   'Electronic check': 0,
                   'Mailed check': 0, }.get(x),
}

for col in df.columns:
    if col not in ['customerID', 'SeniorCitizen']:
        df[col] = df[col].apply(column_lambda_funcs[col])

# RENAME columns
df.rename(
    columns={'gender': 'Female',
             'tenure': 'Tenure',
             'customerID': 'CustomerID',
             'PaymentMethod': 'AutoPayment'},
    inplace=True
)

# Predictors - Target split
X = df.drop(['CustomerID', 'Churn'], axis=1)
y = df['Churn']


# Pipeline
model = Pipeline(
    steps=[
        ('standardize', StandardScaler()),
        ('logreg',
            LogisticRegression(penalty='l2', C=0.043, solver='liblinear')),
    ]
)

# Fit
model.fit(X, y)

# Dump Model
pickle.dump(model, open('model.pkl', 'wb'))
