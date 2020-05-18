import pandas as pd
import uuid

FNAME_IN = '../data_files/Concrete_Data.xls'
FNAME_OUT = '../data_files/concrete_data_full.csv'

df = pd.read_excel(FNAME_IN)

## Original Column Names
# ['Cement (component 1)(kg in a m^3 mixture)',
#  'Blast Furnace Slag (component 2)(kg in a m^3 mixture)',
#  'Fly Ash (component 3)(kg in a m^3 mixture)',
#  'Water  (component 4)(kg in a m^3 mixture)',
#  'Superplasticizer (component 5)(kg in a m^3 mixture)',
#  'Coarse Aggregate  (component 6)(kg in a m^3 mixture)',
#  'Fine Aggregate (component 7)(kg in a m^3 mixture)',
#  'Age (day)',
#  'Concrete compressive strength(MPa, megapascals) ']

# Rename columns
df.columns = [
    'cement',
    'blast_furnace_slag',
    'fly_ash',
    'water',
    'superplasticizer',
    'coarse_aggregate',
    'fine_aggregate',
    'age',
    'concrete_compressive_strength',
]

# Shuffle Data
df = df.sample(frac=1).reset_index(drop=True)

# Add uuid
df['mixture_uuid'] = df.apply(lambda _: uuid.uuid4(), axis=1)

## Add Ratios
df['ratio_water_cement'] = df['water'] / df['cement']
df['ratio_coarse_fine_agg'] = df['coarse_aggregate'] / df['fine_aggregate']

# Reorder columns
ordered_columns = [
    'mixture_uuid',
    'cement',
    'blast_furnace_slag',
    'fly_ash',
    'water',
    'superplasticizer',
    'coarse_aggregate',
    'fine_aggregate',
    'age',
    'ratio_water_cement',
    'ratio_coarse_fine_agg',
    'concrete_compressive_strength',
]

df = df[ordered_columns]

# Save CSV
df.to_csv(FNAME_OUT, index=False)


