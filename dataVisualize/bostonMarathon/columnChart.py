# tool : Jupyter Notebook

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV files
marathon_2015_2017 = pd.read_csv("./dataVisualize/bostonMarathon/data/marathon_2015_2017.csv")

# Select runners from USA by conditional expression
USA_runner = marathon_2015_2017[marathon_2015_2017.Country == "USA"]

# Configure figure size
plt.figure(figsize=(20,10))

# Number of Runner by State - USA
runner_state = sns.countplot('State',data = USA_runner)
runner_state.set_title('Number of Runner by State - USA', fontsize=18)
runner_state.set_xlabel('State', fontdict= {'size':16})
runner_state.set_ylabel('Number of Runner', fontdict= {'size':16})
plt.show()

# Number of Runner by State, Gender - USA
plt.figure(figsize=(20,10))
runner_state = sns.countplot('State',data=USA_runner, hue='M/F',  palette={'F':'r','M':'b'})
runner_state.set_title('Number of Runner by State, Gender - USA', fontsize=18)
runner_state.set_xlabel('State', fontdict= {'size':16})
runner_state.set_ylabel('Number of Runner', fontdict= {'size':16})
plt.show()

# Number of Runner by State, year - USA
plt.figure(figsize=(20,10))
runner_state = sns.countplot('State',data=USA_runner, hue='Year')
runner_state.set_title('Number of Runner by State, year - USA', fontsize=18)
runner_state.set_xlabel('State', fontdict= {'size':16})
runner_state.set_ylabel('Number of Runner', fontdict= {'size':16})
plt.show()
