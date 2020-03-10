import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV files 
marathon_2015_2017 = pd.read_csv("./dataVisualize/bostonMarathon/data/marathon_2015_2017.csv")

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'Male', 'Female'

# only "explode" the 2nd slice (i.e. 'Female')
explode = (0, 0.1)  

# Configure figure size
plt.figure(figsize=(7,7))

# Creae pie Chart
plt.pie(marathon_2015_2017['M/F'].value_counts(), explode=explode, labels=labels, startangle = 90, shadow=True, autopct='%.1f')

# Generate labels and title
plt.title("Male vs Female",fontsize=18)

# Show plot
plt.show()
