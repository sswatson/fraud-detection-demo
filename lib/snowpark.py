snowpark_simple = """
import snowflake.snowpark as snowpark
from snowflake.snowpark.functions import col

import pandas as pd
import xgboost as xgb
from sklearn.metrics import precision_score, recall_score, roc_auc_score, accuracy_score, f1_score
from sklearn.model_selection import train_test_split

def main(session: snowpark.Session):
    # Load data
    data = session.table("simple_features")
    data_df = data.to_pandas()

    # Drop the 'USER_ID' column and separate features from labels
    X = data_df.drop(columns=['USER_ID', 'FRAUDSTER'])
    y = data_df['FRAUDSTER']

    # Train-test split
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dval = xgb.DMatrix(X_val, label=y_val)
    params = {
        "objective": "binary:logistic",
        "eval_metric": "logloss",
        "seed": 42,
    }
    evallist = [(dtrain, 'train'), (dval, 'eval')]
    model = xgb.train(params, dtrain, num_boost_round=100, evals=evallist)

    # Make predictions
    y_pred_proba = model.predict(dval)
    y_pred = [1 if prob > 0.5 else 0 for prob in y_pred_proba]

    # Create a dataframe with metrics
    metrics = pd.DataFrame({
        "Metric": ["Precision", "Recall", "AUC", "Accuracy", "F1 Score"],
        "Value": [
            precision_score(y_val, y_pred),
            recall_score(y_val, y_pred),
            roc_auc_score(y_val, y_pred_proba),
            accuracy_score(y_val, y_pred),
            f1_score(y_val, y_pred)
        ]
    })

    return session.create_dataframe(metrics)
"""

snowpark_graph = """
import this
"""