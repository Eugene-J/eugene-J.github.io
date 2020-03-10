import pandas as pd
import numpy as np

marathon_2015 = pd.read_csv("./dataVisualize/bostonMarathon/data/marathon_results_2015.csv")
marathon_2016 = pd.read_csv("./dataVisualize/bostonMarathon/data/marathon_results_2016.csv")
marathon_2017 = pd.read_csv("./dataVisualize/bostonMarathon/data/marathon_results_2017.csv")

# Add Year column to the CSV files "marathon_results_2015 ~ 2017.csv"
marathon_2015['Year'] = '2015'
marathon_2016['Year'] = '2016'
marathon_2017['Year'] = '2017'

# Merge 2015, 2016 and 2017 files into marathon_2015_2017 file
marathon_2015_2017 = pd.concat([marathon_2015, marathon_2016, marathon_2017], ignore_index=True, sort=False)

#Drop unnecessary columns 
marathon_2015_2017 = marathon_2015_2017.drop(['Unnamed: 0','Bib', 'Citizen', 'Unnamed: 9', 'Proj Time', 'Unnamed: 8'], axis='columns')

# Convert using pandas to_timedelta method
marathon_2015_2017['5K'] = pd.to_timedelta(marathon_2015_2017['5K'])
marathon_2015_2017['10K'] = pd.to_timedelta(marathon_2015_2017['10K'])
marathon_2015_2017['15K'] = pd.to_timedelta(marathon_2015_2017['15K'])
marathon_2015_2017['20K'] = pd.to_timedelta(marathon_2015_2017['20K'])
marathon_2015_2017['Half'] = pd.to_timedelta(marathon_2015_2017['Half'])
marathon_2015_2017['25K'] = pd.to_timedelta(marathon_2015_2017['25K'])
marathon_2015_2017['30K'] = pd.to_timedelta(marathon_2015_2017['30K'])
marathon_2015_2017['35K'] = pd.to_timedelta(marathon_2015_2017['35K'])
marathon_2015_2017['40K'] = pd.to_timedelta(marathon_2015_2017['40K'])
marathon_2015_2017['Pace'] = pd.to_timedelta(marathon_2015_2017['Pace'])
marathon_2015_2017['Official Time'] = pd.to_timedelta(marathon_2015_2017['Official Time'])

# Convert time to seconds value using astype method
marathon_2015_2017['5K'] = marathon_2015_2017['5K'].astype('m8[s]').astype(np.int64)
marathon_2015_2017['10K'] = marathon_2015_2017['10K'].astype('m8[s]').astype(np.int64)
marathon_2015_2017['15K'] = marathon_2015_2017['15K'].astype('m8[s]').astype(np.int64)
marathon_2015_2017['20K'] = marathon_2015_2017['20K'].astype('m8[s]').astype(np.int64)
marathon_2015_2017['Half'] = marathon_2015_2017['Half'].astype('m8[s]').astype(np.int64)
marathon_2015_2017['25K'] = marathon_2015_2017['25K'].astype('m8[s]').astype(np.int64)
marathon_2015_2017['30K'] = marathon_2015_2017['30K'].astype('m8[s]').astype(np.int64)
marathon_2015_2017['35K'] = marathon_2015_2017['35K'].astype('m8[s]').astype(np.int64)
marathon_2015_2017['40K'] = marathon_2015_2017['40K'].astype('m8[s]').astype(np.int64)
marathon_2015_2017['Pace'] = marathon_2015_2017['Pace'].astype('m8[s]').astype(np.int64)
marathon_2015_2017['Official Time'] = marathon_2015_2017['Official Time'].astype('m8[s]').astype(np.int64)

# Save to CSV file "marathon_2015_2017.csv"
marathon_2015_2017.to_csv("./dataVisualize/bostonMarathon/data/marathon_2015_2017.csv", index = None, header=True)
