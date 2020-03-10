import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV files "marathon_results_2015 ~ 2017.csv" under "data" folder
marathon_2015_2017 = pd.read_csv("./dataVisualize/bostonMarathon/data/marathon_2015_2017.csv")

# Select male and female runners by conditional expression
MALE_runner = marathon_2015_2017[marathon_2015_2017['M/F'] == 'M']
FEMALE_runner = marathon_2015_2017[marathon_2015_2017['M/F'] == 'F']

# Configure figure size
plt.figure(figsize=(20,20))

# Set MALE_runner.Age as x_male
x_male = MALE_runner.Age

# Set MALE_runner Official Time as y_male
y_male = MALE_runner['Official Time']

# Set FEMALE_runner.Age as x_male
x_female = FEMALE_runner.Age

# Set FEMALE_runner Official Time as y_male
y_female = FEMALE_runner['Official Time']

# Creae Charts
plt.plot(x_male, y_male, '.', color='b', alpha=0.5)
plt.plot(x_female, y_female, '.', color='r', alpha=0.5)

# Generate labels and title
plt.xlabel("Age", fontsize=16)
plt.ylabel("Official Time (Second)",fontsize=16)
plt.title("Distribution by Running Time and Age",fontsize=20)

# Show plot
plt.show()
