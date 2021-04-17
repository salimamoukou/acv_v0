from acv_explainers import ACVTree
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
import random
import time
import pstats, cProfile

random.seed(2021)

np.random.seed(2021)
data_frame = pd.read_csv('/home/samoukou/Documents/ACV/data/lucas0_train.csv')

y = data_frame.Lung_cancer.values
data_frame.drop(['Lung_cancer'], axis=1, inplace=True)

forest = RandomForestClassifier(n_estimators=5, min_samples_leaf=2, random_state=212, max_depth=8)
forest.fit(data_frame, y)
acvtree = ACVTree(forest, data_frame.values)

X = np.array(data_frame.values, dtype=np.float)[:100]
data = np.array(data_frame.values, dtype=np.float)


def test_sv_cyext():
    cy = acvtree.cyext_shap_values(X, [[]], 5)
    py = acvtree.shap_values(X, [[]])
    assert np.allclose(cy, py)


def test_sv_cyext_coalition():
    cy = acvtree.cyext_shap_values(X, [[0, 1, 2, 3]], 5)
    py = acvtree.shap_values(X, [[0, 1, 2, 3]])
    assert np.allclose(cy, py)


def test_sv_acv_cyext():
    cy = acvtree.cyext_shap_values_acv(X, list(range(8)), list(range(8, 11)), [[]], 5)
    py = acvtree.shap_values_acv(X, list(range(8)), list(range(8, 11)), [[]])
    assert np.allclose(cy, py)


def test_sv_acv_cyext_coalition():
    cy = acvtree.cyext_shap_values_acv(X, list(range(8)), list(range(8, 11)),
                                       [[0, 1, 2, 3]], 5)
    py = acvtree.shap_values_acv(X, list(range(8)), list(range(8, 11)), [[0, 1, 2, 3]])
    assert np.allclose(cy, py)


def test_sdp_cyext():
    cy = acvtree.cyext_compute_sdp_clf(X, S=np.array([0, 1]), data=data, num_threads=5)
    cy_cat = acvtree.cyext_compute_sdp_clf_cat(X, S=np.array([0, 1]), data=data, num_threads=5)

    py = acvtree.compute_sdp_clf(X, S=[0, 1], data=data)
    py_cat = acvtree.compute_sdp_clf_cat(X, S=[0, 1], data=data)

    assert np.allclose(cy, py)
    assert np.allclose(cy_cat, py_cat)


def test_exp_cyext():
    cy = acvtree.cyext_compute_exp(X, S=np.array([0, 1]), data=data, num_threads=5)
    cy_cat = acvtree.cyext_compute_exp_cat(X, S=np.array([0, 1]), data=data, num_threads=5)

    py = acvtree.compute_exp(X, S=[0, 1], data=data)
    py_cat = acvtree.compute_exp_cat(X, S=[0, 1], data=data)

    assert np.allclose(cy, py)
    assert np.allclose(cy_cat, py_cat)


X_swing = X[50:100]


# def test_swing_sv_cyext():
#     cy = acvtree.cyext_swing_sv_clf(X_swing, data=data, C=[[]], thresholds=0.8,
#                                     num_threads=5)
#     py = acvtree.swing_sv_clf(X=X_swing, data=data, C=[[]], threshold=0.8)
#     assert np.allclose(cy[0], py[0])
#     assert np.allclose(cy[1], py[1])
#     assert np.allclose(cy[2], py[2])