# pitchfx_sql
sql database for pitchfx data

*NOTE 2018.01.21*: data no longer available at http://gd2.mlb.com/components/game/mlb/

### Getting started
Building your personal PitchFX dataset requires scraping the data off the web. I've made the process easy for you by writing a Python script that scrapes the data and organizes it in an SQL database. All you need to do is run a single line of code, providing the beginning and end dates of games you are interested in. For instance, if you want to grab data from all games between March 1, 2008, and May 1, 2008, and place the data in a database called *example.db*, run the following code:

*python ./src/scrape_pitchfx.py 03-01-2008 05-01-2008 example.db 1*

For more detailed explanation on how to download your own SQL database and query it, please read [this notebook](https://github.com/jasonpchang/pitchfx_sql/blob/master/notebooks/getting_started/read_data.ipynb).

### Pitch classification
Unsupervised learning approach to indentifying different pitch types thrown by different pitchers (*notebooks/pitch_classification/pitch_classification.ipynb*).

### Swing prediction
Supervised learning approaches to predicting whether a batter will swing at a pitch or not given pitch trajectory and game situation information (*notebooks/swing_prediction/*).

### Pitch prediction
Ongoing work towards predicting the next pitch thrown by a pitcher (*notebooks/pitch_prediction/*)
