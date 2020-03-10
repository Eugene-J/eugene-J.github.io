import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file
marathon_2015_2017 = pd.read_csv("./dataVisualize/bostonMarathon/data/marathon_2015_2017.csv")

# Select runners from USA by conditional expression
USA_runner = marathon_2015_2017[marathon_2015_2017.County == 'USA']
USA_MALE_runner = USA_runner[USA_runner['M/F'] == 'M']
USA_FEMALE_runner = USA_runner[USA_runner['M/F'] == 'F']

# Configure figure size
plt.figure(figsize=(20,10))

sns.set(style="ticks", palette="pastel")

# Draw a nested boxplot to show Pace by Gender
sns.boxplot(x='M/F', y='Pace',
            palette=["m", "g"], 
            data=USA_runner)  

# Generate USA_MALE_runner_statistics, USA_FEMALE_runner_statistics 
USA_MALE_runner_statistics = USA_MALE_runner['Pace'].describe()
USA_FEMALE_runner_statistics = USA_FEMALE_runner['Pace'].describe()
