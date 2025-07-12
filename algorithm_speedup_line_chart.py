import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from preprocess_data import load_data, save_plot

def create_speedup_line_chart():
    """Create a line chart showing speedup ratios between algorithms across text lengths."""
    # Load the data
    df, _ = load_data()
    
    # Set the style
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Create a figure for the plot
    plt.figure(figsize=(12, 8), dpi=100)
    
    # Define text length categories for the x-axis
    text_lengths = [10000, 50000, 100000]
    
    # Group data by text_length and calculate mean speedup ratios
    grouped = df.groupby('text_length').agg({
        'kmp_vs_naive_stream_speedup_time': 'mean',
        'kmp_normal_vs_naive_normal_speedup_time': 'mean',
        'naive_normal_vs_stream_speedup_time': 'mean',
        'kmp_normal_vs_stream_speedup_time': 'mean'
    }).reset_index()
    
    # Filter for just the text lengths we want to include
    grouped = grouped[grouped['text_length'].isin(text_lengths)]
    grouped = grouped.sort_values('text_length')
    
    # Define colors and labels for the speedup ratio comparisons
    speedup_colors = {
        'kmp_vs_naive_stream_speedup_time': '#1f77b4',         # blue
        'kmp_normal_vs_naive_normal_speedup_time': '#ff7f0e',  # orange
        'naive_normal_vs_stream_speedup_time': '#2ca02c',      # green
        'kmp_normal_vs_stream_speedup_time': '#d62728'         # red
    }
    
    speedup_labels = {
        'kmp_vs_naive_stream_speedup_time': 'KMP Stream vs Naive Stream',
        'kmp_normal_vs_naive_normal_speedup_time': 'KMP Normal vs Naive Normal',
        'naive_normal_vs_stream_speedup_time': 'Naive Normal vs Naive Stream',
        'kmp_normal_vs_stream_speedup_time': 'KMP Normal vs KMP Stream'
    }
    
    # Plot each speedup ratio
    for metric, color in speedup_colors.items():
        plt.plot(
            grouped['text_length'],
            grouped[metric],
            label=speedup_labels[metric],
            color=color,
            marker='o',
            markersize=8,
            linewidth=2
        )
    
    # Add a horizontal line at y=1 to indicate no speedup
    plt.axhline(y=1, color='gray', linestyle='--', alpha=0.7, label='No Speedup (Ratio = 1)')
    
    # Configure the plot
    plt.xlabel('Text Length', fontsize=14)
    plt.ylabel('Speedup Ratio', fontsize=14)
    plt.title('Algorithm Speedup Ratios by Text Length', fontsize=16)
    
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
    save_plot(plt.gcf(), 'algorithm_speedup_comparison.png')

if __name__ == "__main__":
    create_speedup_line_chart()
    print("Algorithm speedup ratio comparison generated successfully!") 