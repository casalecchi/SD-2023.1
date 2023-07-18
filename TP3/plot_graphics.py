# THIS SCRIPT ASSUMES THERE ARE THE FOLLOWING CSVs INSIDE THE DIRECTORY
# scalability_test_1.csv ; scalability_test_2.csv ; scalability_test_3.csv

import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt

ST_1 = pd.read_csv('scalability_test_1.csv', sep = ';')
ST_1_SECONDS = []
for i in range(len(ST_1['Time'])):
    time_str = ST_1['Time'][i][7:]
    hours, minutes, seconds = time_str.split(":")
    seconds, microseconds = seconds.split(".")
    time_duration = timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), microseconds=int(microseconds))
    seconds = time_duration.total_seconds()
    ST_1_SECONDS.append(seconds)

ST_2 = pd.read_csv('scalability_test_2.csv', sep = ';')
ST_2_SECONDS = []
for i in range(len(ST_2['Time'])):
    time_str = ST_2['Time'][i][7:]
    hours, minutes, seconds = time_str.split(":")
    seconds, microseconds = seconds.split(".")
    time_duration = timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), microseconds=int(microseconds))
    seconds = time_duration.total_seconds()
    ST_2_SECONDS.append(seconds)

ST_3 = pd.read_csv('scalability_test_3.csv', sep = ';')
ST_3_SECONDS = []
for i in range(len(ST_3['Time'])):
    time_str = ST_3['Time'][i][7:]
    hours, minutes, seconds = time_str.split(":")
    seconds, microseconds = seconds.split(".")
    time_duration = timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), microseconds=int(microseconds))
    seconds = time_duration.total_seconds()
    ST_3_SECONDS.append(seconds)

# Define the data
data = {
    'Scalability Test': ['ST_1', 'ST_1', 'ST_1', 'ST_1', 'ST_1', \
                         'ST_2', 'ST_2', 'ST_2', 'ST_2', 'ST_2', 'ST_2', \
                         'ST_3', 'ST_3', 'ST_3', 'ST_3', 'ST_3', 'ST_3', 'ST_3'],
    'N': [2, 4, 8, 16, 32, \
          2, 4, 8, 16, 32, 64, \
          2, 4, 8, 16, 32, 64, 128],
    'Time': [timedelta(seconds=ST_1_SECONDS[0]), timedelta(seconds=ST_1_SECONDS[1]), timedelta(seconds=ST_1_SECONDS[2]), timedelta(seconds=ST_1_SECONDS[3]),\
            timedelta(seconds=ST_1_SECONDS[4]), \
            \
            timedelta(seconds=ST_2_SECONDS[0]), timedelta(seconds=ST_2_SECONDS[1]), timedelta(seconds=ST_2_SECONDS[2]), timedelta(seconds=ST_2_SECONDS[3]), \
            timedelta(seconds=ST_2_SECONDS[4]), timedelta(seconds=ST_2_SECONDS[5]), \
            \
            timedelta(seconds=ST_3_SECONDS[0]), timedelta(seconds=ST_3_SECONDS[1]), timedelta(seconds=ST_3_SECONDS[2]), timedelta(seconds=ST_3_SECONDS[3]), \
            timedelta(seconds=ST_3_SECONDS[4]), timedelta(seconds=ST_3_SECONDS[5]), timedelta(seconds=ST_3_SECONDS[6])]
}


# Convert the data to a pandas DataFrame
df = pd.DataFrame(data)

# Group the data by Option
grouped_data = df.groupby('Scalability Test')

# Create the line plot
fig, ax = plt.subplots()

for option, group in grouped_data:
    x = group['N']
    y = group['Time'].dt.total_seconds()
    ax.plot(x, y, marker='o', label=option)

# Set the axis labels and the legend
ax.set_xlabel('N')
ax.set_ylabel('Time (seconds)')
ax.legend()

# Display the plot
plt.show()