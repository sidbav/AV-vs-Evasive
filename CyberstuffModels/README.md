
## Machine Learning Models for Defender

// SUBMITTED MODELS //

### Zoe:

Random Forest (100 estimators, depth 5, < 60% Confidence / Predict Probability -> Malware, > 64% Confidence / Predict Probability -> Goodware) 
[Trained on EMBER 2018] -> Dataset [https://ember.elastic.co/ember_dataset_2018_2.tar.bz2] 

### Mike:

Random Forest (300 estimators, depth 25, <47% Confidence / Predict Probability -> Malware, >=47% Confidence / Predict Probability -> Goodware) 
[Trained on EMBER 2018, BODMAS, Benign-NET] ->
Dataset a. [https://ember.elastic.co/ember_dataset_2018_2.tar.bz2] 
	b. [https://whyisyoung.github.io/BODMAS/]
	c. [https://github.com/bormaa/Benign-NET]

### Pipeline Approach ->

Send to Mike if Zoe confidence in range [60-64%]


### Note: 

Mike is built on top of huge benign software samples to provide minimum false positives.
Feature Extractor for these models: Ember Feature Extractor version 2.

Additional Models Trained and Tested to Build Defender:
SVM, SGD, XGBoost, ExtraTrees, CatBoost, VotingClassifier, LCE

### Suggestions / Additional Work: Add Dike Dataset, EMBER 2017 v1 & v2 and adversarial samples

[Check Sci-kit Learn Standard Documentation for details]

