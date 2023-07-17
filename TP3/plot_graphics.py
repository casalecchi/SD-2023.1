import matplotlib.pyplot as plt
import pandas as pd
from datetime import timedelta, datetime

def calculate_timestamp_difference(log_file_path):
    with open(log_file_path, 'r') as file:
        first_timestamp = None
        last_timestamp = None

        for line in file:
            timestamp_str = line.strip().split(" - ")[1]
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')

            if first_timestamp is None:
                first_timestamp = timestamp
            last_timestamp = timestamp

    if first_timestamp is not None and last_timestamp is not None:
        time_difference = last_timestamp - first_timestamp
        return time_difference

    return None

#print(calculate_timestamp_difference("resultado.txt"))

# Define the data
data = {
    'Option': ['Option 1', 'Option 1', 'Option 1', 'Option 1', 'Option 1', 'Option 2', \
                'Option 2', 'Option 2', 'Option 2', 'Option 2', 'Option 2', 'Option 3', \
                'Option 3', 'Option 3', 'Option 3', 'Option 3', 'Option 3', 'Option 3'],
    'N': [2, 4, 8, 16, 32, 2, 4, 8, 16, 32, 64, 2, 4, 8, 16, 32, 64, 128],
    'Time': [timedelta(seconds=38.291190), timedelta(seconds=78.836230), timedelta(seconds=160.926631), \
            timedelta(seconds=320.516054), timedelta(seconds=642.502914), timedelta(seconds=9.076002), \
            timedelta(seconds=19.240000), timedelta(seconds=39.599009), timedelta(seconds=80.543530), \
            timedelta(seconds=161.813102), timedelta(seconds=325.012244), timedelta(seconds=0.223998), \
            timedelta(seconds=0.883001), timedelta(seconds=1.623001), timedelta(seconds=3.437002), \
            timedelta(seconds=11.782217), timedelta(seconds=23.071997), timedelta(seconds=44.135283)]
}

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data)

# Group the data by Option
grouped_data = df.groupby('Option')

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
