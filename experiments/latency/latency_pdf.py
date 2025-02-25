# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np

# def create_plot(csv_file, chunk_size=5000, output_file='compression_time.pdf'):
#     # Read the CSV file
#     df = pd.read_csv(csv_file)
    
#     # Create figure with specified size and DPI
#     plt.figure(figsize=(12, 6), dpi=100)
    
#     # Colors matching the reference image
#     colors = {
#         'zstd_dict': '#ff0000',    # blue
#         'brotli': '#ff7f0e',       # orange
#         'gzip': '#2ca02c',         # green
#         'zstd': '#1f77b4'          # blue
#     }
    
#     # Process each column
#     columns = ['zstd Time', 'brotli Time', 'gzip Time', 'zstd_dict Time']
#     labels = ['Zstd', 'Brotli', 'Gzip', 'Co4U']
    
#     max_chunks = 0  # Track the maximum number of chunks
    
#     for col, label in zip(columns, labels):
#         # Calculate means for each chunk
#         data = df[col].values
#         n_chunks = len(data) // chunk_size + (1 if len(data) % chunk_size != 0 else 0)
#         max_chunks = max(max_chunks, n_chunks)  # Update maximum chunks
#         means = []
        
#         for i in range(n_chunks):
#             start_idx = i * chunk_size
#             end_idx = min((i + 1) * chunk_size, len(data))
#             chunk_mean = np.mean(data[start_idx:end_idx])
#             means.append(chunk_mean)
        
#         # Create x-axis values starting from 0
#         x_values = np.arange(len(means))
        
#         # Plot the line
#         plt.plot(x_values, means, label=label, color=colors[col.split()[0].lower()], linewidth=1.5)
    
#     # Customize the plot
#     plt.grid(True, linestyle='--', alpha=0.7)
#     plt.xlabel('File Number (5k)')
#     plt.ylabel('Latency Time (ms)')
    
#     # Set x-axis limits to start from 0 and end at max chunks
#     plt.xlim(0, max_chunks - 1)
    
#     # Move legend to the right center position
#     plt.legend(title='Compression Methods', bbox_to_anchor=(0.83, 0.6), loc='center left')
    
#     # Adjust layout to prevent legend cutoff
#     plt.tight_layout()
    
#     # Save the plot as PDF with extra space for legend
#     plt.savefig(output_file, format='pdf', bbox_inches='tight')

# # Example usage
# create_plot('multi_folder_ratio_times_2.csv')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

def create_plot(csv_file, output_file='compression_time.pdf'):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Create figure with specified size and DPI
    plt.figure(figsize=(12, 6), dpi=100)
    
    # Colors matching the reference image
    colors = {
        'zstd_dict': '#ff0000',    # blue
        'brotli': '#ff7f0e',       # orange
        'gzip': '#2ca02c',         # green
        'zstd': '#1f77b4'          # blue
    }
    
    # Process each column
    columns = ['zstd Time', 'brotli Time', 'gzip Time', 'zstd_dict Time']
    labels = ['Zstd', 'Brotli', 'Gzip', 'Co4U']
    
    # Get the maximum length for x-axis
    max_length = 0
    
    for col, label in zip(columns, labels):
        # Get the data
        data = df[col].values
        max_length = max(max_length, len(data))
        
        # Apply Savitzky-Golay filter for smoothing
        # window_length must be odd and less than data length
        window_length = min(101, len(data) - (1 if len(data) % 2 == 0 else 0))
        if window_length % 2 == 0:
            window_length -= 1
        
        smooth_data = savgol_filter(data, window_length=window_length, polyorder=3)
        
        # Create x-axis values starting from 0
        x_values = np.arange(len(smooth_data))
        
        # Plot the smoothed line
        plt.plot(x_values, smooth_data, 
                label=label, 
                color=colors[col.split()[0].lower()], 
                linewidth=1.5)
    
    # Customize the plot
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlabel('File Number')
    plt.ylabel('Latency Time (ms)')
    
    # Set x-axis limits to start from 0
    plt.xlim(0, max_length - 1)
    
    # Move legend to the right center position
    plt.legend(title='Compression Methods', 
              bbox_to_anchor=(0.83, 0.6), 
              loc='center left')
    
    # Adjust layout to prevent legend cutoff
    plt.tight_layout()
    
    # Save the plot as PDF with extra space for legend
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.close()

# Example usage
create_plot('multi_folder_ratio_times_2.csv')