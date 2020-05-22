# Concrete Compressive Strength (MPa)


### BACKGROUND
Predicting the Compressive Strength (MPa) of concrete. Dataset is from UCI Machine Learning Repository – contains 7 component features (all measured in density) that make up the concrete mixtures, plus their age (days) and the target variable itself compressive strength (measured in Mega-Pascals). 

_The random forest model used had a mean squared error of approximately 26 MPa_


### CONTENTS OF THIS DIRECTORY
* exploration.ipynb (Exploratory Data Analysis)
* data_scripts
	- ../utils.py
	- ../clean_data.py
	- ../train_model.py
	- ../predictions.py
	- ../sample_queries.sql


### DATA SUMMARY
http://archive.ics.uci.edu/ml/datasets/Concrete+Compressive+Strength
* Number of instances (observations): 1030
* Number of Attributes: 9
* Attribute breakdown: 8 quantitative input variables, and 1 quantitative output variable
* Missing Attribute Values: None


### VARIABLE INFORMATION
Name -- Data Type -- Measurement -- Description

* Cement (component 1) -- quantitative -- kg in a m3 mixture -- Input Variable
* Blast Furnace Slag (component 2) -- quantitative -- kg in a m3 mixture -- Input Variable
* Fly Ash (component 3) -- quantitative -- kg in a m3 mixture -- Input Variable
* Water (component 4) -- quantitative -- kg in a m3 mixture -- Input Variable
* Superplasticizer (component 5) -- quantitative -- kg in a m3 mixture -- Input Variable
* Coarse Aggregate (component 6) -- quantitative -- kg in a m3 mixture -- Input Variable
* Fine Aggregate (component 7) -- quantitative -- kg in a m3 mixture -- Input Variable
* Age -- quantitative -- Day (1 to 365) -- Input Variable
* Concrete compressive strength -- quantitative -- MPa -- Output Variable


### PRE-WORK

After downloading the data, I renamed the columns, added a mixture_uuid (primary key) plus 2 additional features { ratio_water_cement, ratio_coarse_fine_agg } and put the data in a Postgres DB.