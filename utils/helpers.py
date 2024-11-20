import pandas as pd
from sklearn.preprocessing import LabelEncoder


# Function for Label Encoding
def label_encode(df, columns_to_encode):
    le = LabelEncoder()
    label_mappings = {}
    for col in columns_to_encode:
        df[col] = le.fit_transform(df[col])
        label_mappings[col] = dict(zip(le.classes_, le.transform(le.classes_)))
    return df, label_mappings
