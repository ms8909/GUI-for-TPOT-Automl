import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import RFE
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline, make_union
from tpot.builtins import StackingEstimator
from xgboost import XGBClassifier

# NOTE: Make sure that the class is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1).values
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'].values, random_state=None)

# Average CV score on the training set was:0.9913043478260869
exported_pipeline = make_pipeline(
    RFE(estimator=ExtraTreesClassifier(criterion="gini", max_features=1.0, n_estimators=100), step=0.25),
    StackingEstimator(estimator=XGBClassifier(learning_rate=0.1, max_depth=7, min_child_weight=2, n_estimators=100, nthread=1, subsample=0.8)),
    KNeighborsClassifier(n_neighbors=86, p=2, weights="distance")
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
