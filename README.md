# pitchfx_sql
Solve baseball-related problems with your own PitchFX database using Python and SQL

*NOTE 2018.01.21*: data no longer available at http://gd2.mlb.com/components/game/mlb/  

## Getting started
Building your personal PitchFX dataset requires scraping the data off the web. I've made the process easy for you by writing a Python script that scrapes the data and organizes it in an SQL database. All you need to do is run a single line of code, providing the beginning and end dates of games you are interested in. For instance, if you want to grab data from all games between March 1, 2008, and May 1, 2008, and place the data in a database called *example.db*, run the following code:

*python ./src/scrape_pitchfx.py 03-01-2008 05-01-2008 example.db 1*

* For more detailed explanation on how to download your own SQL database and query it, please read [read_data.ipynb](https://github.com/jasonpchang/pitchfx_sql/blob/master/notebooks/getting_started/read_data.ipynb)

* For a look at some of the pitch data available, have a look at exploratory data analysis in [eda.ipynb](https://github.com/jasonpchang/pitchfx_sql/blob/master/notebooks/getting_started/eda.ipynb)  


## Projects
This repository contains a collection of notebooks that serve dual purposes. First, they provide examples of how to interact with the database to extract the information you want. Second, they provide examples of problems that can be addressed using this rich database.

### Pitch classification
Pitchers are characterized by the pitches they throw. Some throw many types of pitches, while some throw few types. Some throw hard, some throw soft. Containing a wealth of pitch trajectory information, the PitchFX database is ideal for classifying what sort of pitches pitchers have at their disposal.

Here, I take an unsupervised learning approach to identify different pitch types thrown by different pitchers. I investigate the effectiveness of hierarchical, K-means, and DBSCAN (standard and multi-density) clustering approaches to grouping pitches. Because the number of types of pitches thrown varies from pitcher to pitcher, I suggest a DBSCAN with K-means clustering approach to automatic pitch clustering.

* Details of the pitch clustering process are outlined in [pitch_classification.ipynb](https://github.com/jasonpchang/pitchfx_sql/blob/master/notebooks/pitch_classification/pitch_classification.ipynb)

* Details of multi-density DBSCAN approach are outlined in [multidensity_dbscan.ipynb](https://github.com/jasonpchang/pitchfx_sql/blob/master/notebooks/pitch_classification/multidensity_dbscan.ipynb)  


### Swing prediction
Predicting when a batter is more likely to swing at a pitch can be useful for a pitcher. For instance, it can be useful to determine how likely a batter will swing on a full count. If he is inclined to swing, then the batter could be susceptible to chasing pitches out of the strike zone.

Here, I take a supervised learning approach to predicting whether a batter will swing at a pitch based on pitch trajectory and game situation information from Pitchf/x. The binary classification models I test are logistic regression, naive Bayes, K-nearest neighbors, support vector machines, and random forest. ROC curves suggest that random forest is the best model.

* Details of the exploratory data analysis for swing prediction is found in [swing_prediction_eda.ipynb](https://github.com/jasonpchang/pitchfx_sql/blob/master/notebooks/swing_prediction/swing_prediction_eda.ipynb)

* Details of swing prediction using different subsets of data to build random forest models are outlined in [swing_prediction_random_forest.ipynb](https://github.com/jasonpchang/pitchfx_sql/blob/master/notebooks/swing_prediction/swing_prediction_random_forest.ipynb)

* Details of swing prediction using various models are outlined in [swing_prediction_models.ipynb](https://github.com/jasonpchang/pitchfx_sql/blob/master/notebooks/swing_prediction/swing_prediction_models.ipynb)
