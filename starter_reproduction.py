# ANLY 735 Week 6 — Starter Artifact
# Run this file BEFORE changing the model specification.

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_auc_score, accuracy_score
import sklearn
import sys

data = load_breast_cancer()
X, y = data.data, data.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.30,
    stratify=y,
    random_state=735
)

# Model specification as documented in the supplied artifact.
model = DecisionTreeClassifier(random_state=735)

model.fit(X_train, y_train)

prob = model.predict_proba(X_test)[:, 1]
pred = model.predict(X_test)

auc = roc_auc_score(y_test, prob)
accuracy = accuracy_score(y_test, pred)

print("Python:", sys.version.split()[0])
print("scikit-learn:", sklearn.__version__)
print("Dataset rows:", X.shape[0])
print("Dataset features:", X.shape[1])
print("Train rows:", X_train.shape[0])
print("Test rows:", X_test.shape[0])
print(f"ROC AUC: {auc:.4f}")
print(f"Accuracy: {accuracy:.4f}")
