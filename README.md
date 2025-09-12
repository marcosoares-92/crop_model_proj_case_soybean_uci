# Model Project using Industrial Data Science Workflow in Crop Science

	- IDSW in: https://github.com/marcosoares-92/IndustrialDataScienceWorkflow
	- IDSW in PyPI: https://pypi.org/project/idsw/
	- IDSW ETL Workflow: https://github.com/marcosoares-92/IndustrialDataScience_ETL_Workflow
	- IDSW Modelling Workflow: https://github.com/marcosoares-92/IndustrialDataScience_ML_Modelling_Workflow

### Exploratory Data Analysis: understanding the variables, collinearity, frequency information and covariates.
### Unsupervised Modelling with K-Means Clustering
### Modelling with XGBoost: Feature Importance Ranking and SHAP analysis
### Modelling with several TensorFlow Algorithms

# Dataset used: Forty Soybean Cultivars from Subsequent Harvests (UCI Repository)

	- Dataset official Repository: https://archive.ics.uci.edu/dataset/913/forty+soybean+cultivars+from+subsequent+harvests
	- Original paper: https://doi.org/10.46420/TAES.e230005

- Donated on 10/28/2023
- Description: Soybean cultivation is one of the most important because it is used in several segments of the food industry. The evaluation of soybean cultivars subject to different planting and harvesting characteristics is an ongoing field of research. We present a dataset obtained from forty soybean cultivars planted in subsequent seasons. The experiment used randomized blocks, arranged in a split-plot scheme, with four replications. The following variables were collected: plant height, insertion of the first pod, number of stems, number of legumes per plant, number of grains per pod, thousand seed weight, and grain yield, resulting in 320 data samples. The dataset presented can be used by researchers from different fields of activity.
- Dataset Characteristics: Tabular
- Associated Tasks: Classification, Regression, Clustering, Other
- Feature Type: Real, Categorical, Integer
- Number of Instances: 320
- Number of Features: 11
- Dataset Information from original authors (as in UCI):
	- For what purpose was the dataset created? To study soybean cultivars harvested in subsequent seasons.
	- Who funded the creation of the dataset? There was no cash financing, but support for carrying out the experiments by Accert Pesquisa e Consultoria Agronomia, located in Balsas, Maranhão, Brazil.
	- What do the instances in this dataset represent? The average values of 10 plants per plot at harvest (phase R8).
	- Are there recommended data splits? We recommend that stratified cross-validation be applied, so that the same cultivar does not appear in the training and test sets simultaneously.
	- Does the dataset contain data that might be considered sensitive in any way? No data is confidential
	- Was there any data preprocessing performed? The data presented is raw data
- Has Missing Values? No

Variables Table
Variable Name		Role		Type		Description
Season			Feature		Integer		1 or 2
Cultivar		Feature		Categorical	Cultivar names
Repetition		Feature		Integer		1, 2, 3 or 4
PH			Feature		Continuous	plant height (cm) – determined from the soil surface to the insertion of the last leaf using a millimeter ruler
IFP			Feature		Continuous	insertion of the first pod (cm) – determined from the soil surface to the insertion of the first vegetable
NLP			Feature		Continuous	Number of stems (unit) – through manual counting
NGP			Feature		Continuous	Number of legumes per plant (unit) – through manual counting
NGL			Feature		Continuous	Number of grains per plant (unit) – through manual counting
NS			Feature		Continuous	Number of grains per pod (unit) – through manual counting
MHG			Feature		Continuous	Thousand seed weight (g) – according to the methodology described in Brasil (2009)
GY			Feature		Continuous	Grain yield (kg/ha) – determined by harvesting the useful area of the plot and standardized to a grain moisture level of 13%