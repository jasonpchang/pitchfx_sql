# pitchfx_sql
sql database for pitchfx data

*NOTE 2018.01.21*: data no longer available at http://gd2.mlb.com/components/game/mlb/

### Getting started
Building your personal PitchFX dataset requires scraping the data off the web. I've made the process easy for you by writing a Python script that scrapes the data and organizes it in an SQL database. All you need to do is run a single line of code, providing the beginning and end dates of games you are interested in. For instance, if you want to grab data from all games between March 1, 2008, and May 1, 2008, and place the data in a database called *example.db*, run the following code:

*python ./src/scrape_pitchfx.py 03-01-2008 05-01-2008 example.db 1*

For more detailed explanation on how to download your own SQL database and query it, please read [read_data.ipynb](https://github.com/jasonpchang/pitchfx_sql/blob/master/notebooks/getting_started/read_data.ipynb).

For a look at some of the pitch data available, have a look at exploratory data analysis in [eda.ipynb](https://github.com/jasonpchang/pitchfx_sql/blob/master/notebooks/getting_started/eda.ipynb).


### Projects
This repository contains a collection of notebooks that serve dual purposes. First, they provide examples of how to interact with the database to extract the information you want. Second, they provide examples of questions that can be addressed using this rich database.

##### Pitch classification
Pitchers are characterized by the pitches they throw. Some throw many types of pitches, while some throw few types. Some throw hard, some throw soft. Containing a wealth of pitch trajectory information, the PitchFX database is ideal for classifying what sort of pitches pitchers have at their disposal.

Here, I take an unsupervised learning approach to identify different pitch types thrown by different pitchers. I investigate the effectiveness of hierarchical, K-means, and DBSCAN (standard and multi-density) clustering approaches to grouping pitches. Because the number of types of pitches thrown varies from pitcher to pitcher, I suggest a DBSCAN with K-means clustering approach to automatic pitch clustering.

Details of the pitch clustering process are outlined in [pitch_classification.ipynb](identifying://github.com/jasonpchang/pitchfx_sql/blob/master/notebooks/pitch_classification/pitch_classification.ipynb).

Details of multi-density DBSCAN approach are outlined in [this notebook](https://github.com/jasonpchang/pitchfx_sql/blob/master/notebooks/pitch_classification/multidensity_dbscan.ipynb).

##### Swing prediction
Supervised learning approaches to predicting whether a batter will swing at a pitch or not given pitch trajectory and game situation information (*notebooks/swing_prediction/*).
