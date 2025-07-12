import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from preprocess_data import load_data, save_plot

def create_algorithm_comparison_line_chart():
    """Create a line chart showing time complexity comparison between the 4 algorithms."""
    # Load the data
    df, _ = load_data()
    
    # Set the style
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Create a figure for the plot
    plt.figure(figsize=(12, 8), dpi=100)
    
    # Define colors for the algorithms
    colors = {
        'naive_stream_time_sec': '#1f77b4',  # blue
        'kmp_stream_time_sec': '#ff7f0e',    # orange
        'naive_normal_time_sec': '#2ca02c',  # green
        'kmp_normal_time_sec': '#d62728'     # red
    }
    
    # Define text length categories for the x-axis
    text_lengths = [10000, 50000, 100000]
    
    # Group data by text_length and calculate mean time for each algorithm
    grouped = df.groupby('text_length').agg({
        'naive_stream_time_sec': 'mean',
        'kmp_stream_time_sec': 'mean',
        'naive_normal_time_sec': 'mean',
        'kmp_normal_time_sec': 'mean'
    }).reset_index()
    
    # Filter for just the text lengths we want to include
    grouped = grouped[grouped['text_length'].isin(text_lengths)]
    grouped = grouped.sort_values('text_length')
    
    # Plot each algorithm
    for alg, color in colors.items():
        # Convert algorithm name to a more readable format for the legend
        alg_label = alg.replace('_time_sec', '').replace('_', ' ').title()
        
        plt.plot(
            grouped['text_length'],
            grouped[alg],
            label=alg_label,
            color=color,
            marker='o',
            markersize=8,
            linewidth=2
        )
    
    # Configure the plot
    plt.xlabel('Text Length', fontsize=14)
    plt.ylabel('Time (s)', fontsize=14)
    plt.title('Time Complexity Comparison of Algorithms', fontsize=16)
    
    # Format x-axis ticks to display as text lengths
    plt.xticks(text_lengths, text_lengths, fontsize=12)
    plt.yticks(fontsize=12)
    
    # Add grid
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Add legend with clear labels
    plt.legend(fontsize=12)
    
    # Ensure tight layout
    plt.tight_layout()
    
    # Save the plot
    save_plot(plt.gcf(), 'algorithm_time_comparison.png')

if __name__ == "__main__":
    create_algorithm_comparison_line_chart()
    print("Algorithm time comparison line chart generated successfully!") 