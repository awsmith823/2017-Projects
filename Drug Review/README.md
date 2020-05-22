# Pharma Drug Reviews

### BACKGROUND
Predicting the rating of pharma drug reviews. Transformed the rating system from 1-10 ratings, to a NPS rating system (-1, 0, 1). 

### MODEL: Naive Bayes
_This algorithm is mostly used in text classification and with problems having multiple classes. Easy to build, simple, and particularly useful for very large data sets._

After creating a balanced training dataset with equal distributions for each class, the model acheived a 5-fold CV accuracy score of 56%. This is a significant boost from a baseline accuracy of 33%.

Experiments:
_After a few GridSearch trials, I found that OneHotEncoding the drugNames & conditions was expensive and did not provide a boost in accuracy. Using review unigrams with some document structural features (i.e review_length) performed the best_

### CONTENTS OF THIS DIRECTORY
* EDA - Sample.ipynb (Exploratory Data Analysis)
* data_raw (.gitignored - Download from UCI link below)
* data_derived
	- ../drugsComTrain_balanced.tsv
	- ../ListConditions.txt
	- ../ListDrugs.txt
* create_training_data.py (Create balanced sample from each class)
* train_model.py (Pipeline of transformations & Naive Bayes estimator)
* test_model.py
* utils.py (UDFs)
* settings.py (Constants)
* get_ListConditions.py (Unique conditions from training data)
* get_ListDrugs.py (Unique drugs from training data)


### DATA SUMMARY
http://archive.ics.uci.edu/ml/datasets/Drug+Review+Dataset+%28Drugs.com%29

The dataset provides patient reviews on specific drugs along with related conditions and a 10 star patient rating reflecting overall patient satisfaction. 

Attribute Info
1. drugName (categorical): name of drug 
2. condition (categorical): name of condition 
3. review (text): patient review 
4. rating (numerical): 10 star patient rating 
5. date (date): date of review entry 
6. usefulCount (numerical): number of users who found review useful