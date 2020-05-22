import sys
import pandas as pd
import numpy as np
import pickle
import psycopg2
sys.path.append('..')
from utils import config
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

MODEL_FNAME = 'model.pkl'

# Load model
with open(MODEL_FNAME, 'rb') as file:  
    model = pickle.load(file)

# Obtain the configuration parameters
params = config()
# Connect to the PostgreSQL database
conn = psycopg2.connect(**params)
# Create a cursor object
cur = conn.cursor()

# Query the data
sql_query = '''
	SELECT
		mixture_uuid,
		cement,
		blast_furnace_slag,
		fly_ash,
		water,
		superplasticizer,
		coarse_aggregate,
		fine_aggregate,
		age,
		ratio_water_cement,
		ratio_coarse_fine_agg,
		concrete_compressive_strength
	FROM concrete_test_data;
'''

test = pd.read_sql_query(sql_query, conn)

X = test.drop(['mixture_uuid', 'concrete_compressive_strength'], axis=1)
y = test['concrete_compressive_strength']

# Close the cursor and connection to so the server
cur.close()
conn.close()


# Make predictions
test['predict_strength'] = model.predict(
	test.drop(['mixture_uuid', 'concrete_compressive_strength'], axis=1)
)

result_columns = [
	'mixture_uuid', 
	'concrete_compressive_strength', 
	'predict_strength'
]

print(test[result_columns].sample(5))
