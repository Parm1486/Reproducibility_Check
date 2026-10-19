# Reproducibility Investigation Record

**Name:** Parminder Singh
**Date:** October 18, 2026

## 1. Before running the code

What result are you attempting to reconstruct?

The reported test ROC AUC of approximately 0.9053 and accuracy of approximately 0.9301 for a Decision Tree classifier using the Wisconsin Diagnostic Breast Cancer dataset.

What information appears sufficiently documented?

- Dataset loader: `sklearn.datasets.load_breast_cancer()`.
- Predictors and outcome: `data.data` and `data.target`.
- Dataset dimensions: 569 observations and 30 features.
- Train/test split: `test_size=0.30`, `stratify=y`, and `random_state=735`.
- Model: `DecisionTreeClassifier(random_state=735)`, with all other parameters left at library defaults.
- No explicit preprocessing, feature selection, or sample weighting.
- ROC AUC calculation: `roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])`.
- Accuracy calculation: `accuracy_score(y_test, model.predict(X_test))`.

What information might still matter but is not documented?

- The software versions used to generate the earlier reported result.
- Confirmation that the earlier result came from this exact code revision.
- Original training/test observation indices.
- Original test labels, predicted labels, and predicted probabilities.
- Whether the earlier result used a different split, preprocessing procedure, model configuration, sample weighting, or averaging across runs or folds.
- Whether the earlier metrics were rounded to four decimal places or described only as loose approximations.

## 2. Initial execution

**ROC AUC:** 0.9360.
**Accuracy:** 0.9474.
**Match to reported result?** No.

Do not change the code yet. Describe the discrepancy.

The unchanged supplied code produced 398 training observations and 171 test observations. Its ROC AUC exceeded the reported value by approximately 0.0307, and its accuracy exceeded the reported value by approximately 0.0173.

An independent execution in Python: 3.12.2 with scikit-learn: 1.5.1 reproduced these new results.

The accuracy discrepancy provides a stronger diagnostic clue than the score difference alone. With 171 test observations and no sample weights, accuracy must equal an integer divided by 171. No such fraction rounds to 0.9301 at four decimal places:

- 159/171 = 0.9298245614, which rounds to 0.9298.
- 160/171 = 0.9356725146, which rounds to 0.9357.

Consequently, if 0.9301 was reported to four-decimal precision, it cannot come from the supplied unweighted accuracy calculation on this 171-observation test set. This conclusion is weaker if the reported value was intended only as a loose approximation.

## 3. Diagnostic audit

Record each analytical decision you inspect.

| Decision | What the artifact tells you | Could it affect the result? | What did you test? |
|---|---|---|---|
| Dataset | Uses `load_breast_cancer()` and all 30 supplied features. The loaded dataset contains 569 observations. | Yes. Different data, row ordering, filtering, or feature selection could change the split and fitted tree. | Confirmed the loaded dimensions. Retained the supplied data and feature order. No alternative dataset or preprocessing was introduced. |
| Outcome | Uses `data.target`; class 0 is malignant and class 1 is benign. The probability column evaluated is class 1. | Yes. Inconsistent label/probability alignment could change AUC or its interpretation. | Verified the outcome convention and that the supplied scoring procedure evaluates benign-class probabilities. Did not relabel the outcome. |
| Train/test split | Uses a 30% test set, stratification by outcome, and split seed 735. | Yes. Split size and membership affect both model fitting and evaluation. | Reproduced the supplied 398/171 split. Tested 30% without stratification: AUC 0.9168, accuracy 0.9123. Investigated a 25% split because 133/143 rounds to 0.9301: with stratification, AUC 0.9117 and accuracy 0.9231; without stratification, AUC 0.9004 and accuracy 0.8951. None matched the reported pair. |
| Random seed | Both the split and classifier use `random_state=735`. | Yes. The split seed affects observation membership; the tree seed can affect feature ordering and tie-breaking during fitting. However, seed changes cannot make unweighted accuracy on 171 observations round to 0.9301. | Retained both seeds at 735 in every diagnostic run. Did not search alternative seeds. |
| Model specification | Uses `DecisionTreeClassifier(random_state=735)` with other settings left at library defaults. | Yes. Different tree settings or implementation details could change predictions, but cannot independently resolve the 171-observation accuracy inconsistency. | Fitted the documented classifier without changing its hyperparameters. No tuning was performed. |
| Evaluation metric | Computes ROC AUC from class-1 probabilities and accuracy from predicted labels on one holdout set, without sample weights. | Yes. Weighting, fold averaging, different evaluation observations, or a reporting error could explain the denominator inconsistency. | Recalculated both metrics and inspected the confusion matrix: `[[57, 7], [2, 105]]`. Verified 162 correct predictions out of 171. Confirmed that this fitted model's test probabilities were only 0 and 1, so using hard predictions instead would not change its AUC. |
| Software/environment | The code prints Python and scikit-learn versions, but the versions associated with the earlier reported result were not supplied. | Potentially. Version differences can affect fitted results, but cannot remove the integer-denominator constraint for this accuracy calculation. | Independently executed the code in Python 3.12.8 and scikit-learn 1.6.1. No cross-version reconstruction was performed. |

## 4. Reconstruction

What change did you make, and why was it defensible?

No change was adopted as a successful reconstruction.

The investigation tested split-related alternatives while retaining the dataset, classifier, and both seeds. A 25% test split was investigated because it creates 143 test observations, and 133/143 = 0.9300699301 rounds to the reported accuracy of 0.9301. This supplied a numerical rationale for the diagnostic test, but did not establish that a 25% split was historically used. Other test-set denominators can also yield an accuracy rounding to 0.9301.

Omission of stratification was also checked as a possible split-specification mismatch. Neither change, separately or together, recovered the reported metric pair.

No seed search or hyperparameter search was undertaken. The original supplied specification was retained as the verified baseline rather than presenting an unsupported score-matching modification.

**Final model specification:** Verified baseline only: `DecisionTreeClassifier(random_state=735)`, fitted to all 30 features using `train_test_split(test_size=0.30, stratify=y, random_state=735)`. No successfully reconstructed specification for the earlier reported result was identified.

**ROC AUC:** Verified baseline: 0.9360. Earlier target of approximately 0.9053 was not reconstructed.

**Accuracy:** Verified baseline: 0.9474. Earlier target of approximately 0.9301 was not reconstructed.

## 5. Verdict

Not reproducible as supplied.

Justification:

The supplied code executes successfully and independently reproduces the new result. It does not reproduce the earlier reported result.

Assuming conventional four-decimal reporting, the earlier accuracy is incompatible with unweighted evaluation on the supplied 171-observation test set. Evidence-motivated checks of split size and stratification did not reconstruct the reported pair.

The materials therefore support reproduction of the supplied code's current output, but are insufficient to reconstruct the earlier reported result or establish the analytical pathway that produced it. A numerical match obtained through additional unconstrained searching would not establish that pathway.

## 6. Reflection

What is the smallest missing detail that meaningfully affected reproducibility, and what should have been reported?

The investigation did not identify one confirmed missing historical decision. The smallest immediately decisive missing detail is the evaluation denominator and aggregation method associated with the earlier accuracy: how many observations were evaluated, and whether 0.9301 represented a single unweighted holdout accuracy or an average or weighted statistic.

The exact original train/test indices would be the most useful compact record for reconstructing a single-holdout analysis. The split fraction alone would not establish test membership.

The original report should have included:

- Training and test counts and class distributions.
- Exact split settings and saved observation indices.
- Full model parameters and software versions.
- Explicit metric definitions, positive-class convention, and any weighting or averaging.
- Saved test labels, predicted labels, and predicted probabilities.
- The code revision associated with the reported output.

The central lesson is that a plausible score is not evidence of a reproduced analytical pathway. Where provenance is missing, documenting non-reproduction is more defensible than modifying the analysis until its scores resemble the target.
