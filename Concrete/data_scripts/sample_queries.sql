/* 
The following sample queries were used to create tables in the
ConcreteData DB and do some light exploration of the columns
*/


DROP TABLE IF EXISTS concrete_data;
CREATE TABLE concrete_data (
	mixture_uuid VARCHAR(64) PRIMARY KEY,
	cement FLOAT(4),
	blast_furnace_slag FLOAT(4),
	fly_ash FLOAT(4),
	water FLOAT(4),
	superplasticizer FLOAT(4),
	coarse_aggregate FLOAT(4),
	fine_aggregate FLOAT(4),
	age SMALLINT,
	ratio_water_cement FLOAT(4),
	ratio_coarse_fine_agg FLOAT(4),
	concrete_compressive_strength FLOAT(4)
);

-- COPY COMMAND (Getting csv data to populate DB table)

-- After concrete_data is populated, sample it to get testing data
DROP TABLE IF EXISTS concrete_test_data;
CREATE TABLE concrete_test_data (
	mixture_uuid VARCHAR(64) PRIMARY KEY,
	cement FLOAT(4),
	blast_furnace_slag FLOAT(4),
	fly_ash FLOAT(4),
	water FLOAT(4),
	superplasticizer FLOAT(4),
	coarse_aggregate FLOAT(4),
	fine_aggregate FLOAT(4),
	age SMALLINT,
	ratio_water_cement FLOAT(4),
	ratio_coarse_fine_agg FLOAT(4),
	concrete_compressive_strength FLOAT(4)
);

WITH test_samples AS (
	SELECT
		mixture_uuid
		, cement
		, blast_furnace_slag
		, fly_ash
		, water
		, superplasticizer
		, coarse_aggregate
		, fine_aggregate
		, age
		, ratio_water_cement
		, ratio_coarse_fine_agg
		, concrete_compressive_strength
	FROM concrete_data
	ORDER BY RANDOM()
	LIMIT ((SELECT COUNT(mixture_uuid) FROM concrete_data)*0.20)::int
)

INSERT INTO concrete_test_data
SELECT *
FROM test_samples;

-- Use the uuids from test samples to get train samples via exclusion
DROP TABLE IF EXISTS concrete_train_data;
CREATE TABLE concrete_train_data (
	mixture_uuid VARCHAR(64) PRIMARY KEY,
	cement FLOAT(4),
	blast_furnace_slag FLOAT(4),
	fly_ash FLOAT(4),
	water FLOAT(4),
	superplasticizer FLOAT(4),
	coarse_aggregate FLOAT(4),
	fine_aggregate FLOAT(4),
	age SMALLINT,
	ratio_water_cement FLOAT(4),
	ratio_coarse_fine_agg FLOAT(4),
	concrete_compressive_strength FLOAT(4)
);

WITH train_samples AS (
	SELECT
		mixture_uuid
		, cement
		, blast_furnace_slag
		, fly_ash
		, water
		, superplasticizer
		, coarse_aggregate
		, fine_aggregate
		, age
		, ratio_water_cement
		, ratio_coarse_fine_agg
		, concrete_compressive_strength
	FROM concrete_data
	WHERE mixture_uuid NOT IN (
		SELECT mixture_uuid FROM concrete_test_data
	)
)

INSERT INTO concrete_train_data
SELECT *
FROM train_samples;



/* Exploratory SQL Queries*/

-- Count rows in each table
WITH row_counts AS (
	SELECT 
		'1) full data' AS category
		, COUNT(*) AS num_rows
	FROM concrete_data
 UNION
	SELECT 
		'2) train data' AS category
		, COUNT(*) AS num_rows
	FROM concrete_train_data
 UNION
	SELECT 
		'3) test data' AS category
		, COUNT(*) AS num_rows
	FROM concrete_test_data
)

SELECT
	category
	, num_rows
	, ROUND((num_rows::float / (MAX(num_rows) OVER()))::decimal,2) AS pct
FROM row_counts
ORDER BY category;

-- Summary Stats for strength ~ c(age, ratio_water_cement)
WITH summary AS (
	SELECT 
		width_bucket(concrete_compressive_strength, 0, 100, 5) AS strength_bucket
		, COUNT(*) AS frequency
		, PERCENTILE_DISC(0.50) WITHIN GROUP (
			ORDER BY age::decimal
		) AS median_age_days
		, PERCENTILE_DISC(0.50) WITHIN GROUP (
			ORDER BY ratio_water_cement::decimal
		) AS median_water_cement_ratio		
	FROM concrete_data
	GROUP BY 1
)

SELECT
	((strength_bucket - 1) * ((100 - 0)/5))::varchar ||' - '|| 
	((strength_bucket) * ((100 - 0)/5))::varchar ||' MPa' AS concrete_strength
	,frequency
	,median_age_days
	,median_water_cement_ratio
FROM summary
ORDER BY 1;

-- Descriptive stats for compressive strength
SELECT 
	ROUND(AVG(concrete_compressive_strength::decimal),3) AS avg_strength
	,ROUND(MIN(concrete_compressive_strength::decimal),3) AS min_strength
	,ROUND(MAX(concrete_compressive_strength::decimal),3) AS max_strength
	,ROUND(PERCENTILE_DISC(0.25) WITHIN GROUP (
		ORDER BY concrete_compressive_strength::decimal
	),3) AS q25_strength	
	,ROUND(PERCENTILE_DISC(0.5) WITHIN GROUP (
		ORDER BY concrete_compressive_strength::decimal
	),3) AS q50_strength
	,ROUND(PERCENTILE_DISC(0.75) WITHIN GROUP (
		ORDER BY concrete_compressive_strength::decimal
	),3) AS q75_strength
FROM concrete_data
LIMIT 5;