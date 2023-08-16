import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import warnings

# Get a list of all CSV files in the directory
csv_files = [file for file in os.listdir('.') if file.endswith('.csv')]

# Create an empty dictionary to store dataframes for each location
dataframes = {}

# Read and process each CSV file
for csv_file in csv_files:
    place_name = csv_file.split('_')[0]  # Extract place name from the file name
    
    # Read the CSV file into a pandas DataFrame
    data = pd.read_csv(csv_file)
    
    # Convert the 'system:time_start' column to datetime format
    data['system:time_start'] = pd.to_datetime(data['system:time_start'])
    
    # Rename columns for easier access
    data.rename(columns={'system:time_start': 'date', 'undefined': 'precp'}, inplace=True)
    
    # Create new columns for year and month
    data['year'] = data['date'].dt.year
    data['month'] = data['date'].dt.month
    
    # Calculate the annual average precipitation
    annual_avg_precipitation = data.groupby('year')['precp'].mean().reset_index()
    
    # Store the dataframe in the dictionary
    dataframes[place_name] = annual_avg_precipitation

# Calculate overall x-axis and y-axis limits
min_year = min([df['year'].min() for df in dataframes.values()])
max_year = max([df['year'].max() for df in dataframes.values()])
max_precip = max([df['precp'].max() for df in dataframes.values()])

# Set up the plot
plt.figure(figsize=(20, 12))
plt.xlabel('Year', fontsize=24)
plt.ylabel('Precipitation (mm)', fontsize=24)
plt.title('Annual Average Precipitation Timeseries', fontsize=24)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlim(min_year, max_year)
plt.ylim(0, max_precip * 1.1)

# Initialize the animation function
def update(frame):
    plt.clf()
    plt.xlabel('Year', fontsize=24)
    plt.ylabel('Precipitation (mm)', fontsize=24)
    plt.title('Annual Average Precipitation Timeseries', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlim(min_year, max_year)
    plt.ylim(0, max_precip * 1.1)
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for place_name, df in dataframes.items():
            plt.plot(df['year'][:frame+1], df['precp'][:frame+1], marker='o', markersize = 16, label=place_name, linewidth=3)
    
    plt.legend(loc='lower left', fontsize=20)  # Set legend position and font size

# Create the animation
ani = FuncAnimation(plt.gcf(), update, frames=range(1, len(dataframes[list(dataframes.keys())[0]])), interval=400)

# Save the animation as a GIF
ani.save('precipitation_animation.gif', writer='pillow')

print("Done!")
