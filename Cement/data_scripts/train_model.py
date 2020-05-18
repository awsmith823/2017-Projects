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

# Obtain the configuration parameters
params = config()
# Connect to the PostgreSQL database
conn = psycopg2.connect(**params)
# Create a cursor object
cur = conn.cursor()

# Query the data
sql_query = '''
	SELECT
		-- mixture_uuid,
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
	FROM concrete_train_data;
'''

train = pd.read_sql_query(sql_query, conn)

# Close the cursor and connection to so the server
cur.close()
conn.close()

# Train model
model = Pipeline(steps=[
    ('normalize', StandardScaler()), 
    ('rf', RandomForestRegressor(
            n_estimators=10, 
            criterion='mse', 
            max_features='sqrt'
        )
    )
])

model.fit(
    X=train.drop(['concrete_compressive_strength'], axis=1),
    y=train['concrete_compressive_strength']
)

# SAVE MODEL
with open(MODEL_FNAME, 'wb') as file:  
    pickle.dump(model, file)

