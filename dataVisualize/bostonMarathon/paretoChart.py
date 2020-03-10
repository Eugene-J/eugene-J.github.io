import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV files
marathon_2015_2017 = pd.read_csv("./dataVisualize/bostonMarathon/data/marathon_2015_2017.csv")

# Select runners from Age 20 to 60 by conditional expression
runner_1860 = marathon_2015_2017[marathon_2015_2017.Age.isin(range(20,60))]

# Create runner_1860_counting Dataframe with counting by Age
runner_1860_counting = runner_1860['Age'].value_counts()

# Store index of runner_1860_counting into x
x = runner_1860_counting.index

# Conver x values to String in order to avoid int sorting
x = [str(i) for i in x]

# Store values of runner_1860_counting into y
y = runner_1860_counting.values

# Calculate ratio and accumulated ratio
ratio = y / y.sum()
ratio_sum = ratio.cumsum()

# Configure figure size
fig, barChart = plt.subplots(figsize=(20,10))

# Creae bar Chart
barChart.bar(x, y)

# Creae line Chart
lineChart = barChart.twinx()
lineChart.plot(x, ratio_sum, '-ro', alpha=0.5)

# Creae right side labels
ranges = lineChart.get_yticks()
lineChart.set_ytickslabels(['{:,.1%}'.format(x) for x in ranges])

# Creae annotations on line chart
ratio_sum_percentages = ['{0:.0%}'.format(x) for x in ratio_sum]

for i, txt in enumerate(ratio_sum_percentages):
    lineChart.annotate(txt, (x[i], ratio_sum[i]), fontsize=14)    
    
# Generate labels and title
barChart.set_xlabel('Age', fontdict= {'size':16})
barChart.set_ylabel('Number of runner', fontdict= {'size':16})
plt.title('Pareto Chart - Number of runner by Age', fontsize=18)

# Show plot
plt.show()
