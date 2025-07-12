import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from preprocess_data import load_data, save_plot

def create_comparisons_line_chart():
    """Create a line chart showing the number of comparisons across algorithms at different text lengths."""
    # Load the data
    df, _ = load_data()
    
    # Set the style
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Create a figure for the plot
    plt.figure(figsize=(12, 8), dpi=100)
    
    # Define colors for the algorithms
    colors = {
        'naive_stream_comparisons': '#1f77b4',  # blue
        'kmp_stream_comparisons': '#ff7f0e',    # orange
        'naive_normal_comparisons': '#2ca02c',  # green
        'kmp_normal_comparisons': '#d62728'     # red
    }
    
    # Define text length categories for the x-axis
    text_lengths = [10000, 50000, 100000]
    
    # Group data by text_length and calculate mean comparisons for each algorithm
    grouped = df.groupby('text_length').agg({
        'naive_stream_comparisons': 'mean',
        'kmp_stream_comparisons': 'mean',
        'naive_normal_comparisons': 'mean',
        'kmp_normal_comparisons': 'mean'
    }).reset_index()
    
    # Filter for just the text lengths we want to include
    grouped = grouped[grouped['text_length'].isin(text_lengths)]
    grouped = grouped.sort_values('text_length')
    
    # Plot each algorithm
    for alg, color in colors.items():
        # Convert algorithm name to a more readable format for the legend
        alg_label = alg.replace('_comparisons', '').replace('_', ' ').title()
        
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
    plt.ylabel('Number of Comparisons', fontsize=14)
    plt.title('Algorithm Comparison Count by Text Length', fontsize=16)
    
    # Format x-axis ticks to display as text lengths
    plt.xticks(text_lengths, text_lengths, fontsize=12)
    plt.yticks(fontsize=12)
    
    # Add grid
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Add legend with clear labels
    plt.legend(fontsize=12)
    
    # Use logarithmic scale for y-axis to better visualize differences
    plt.yscale('log')
    
    # Ensure tight layout
    plt.tight_layout()
    
    # Save the plot
    save_plot(plt.gcf(), 'algorithm_comparisons_count.png')

if __name__ == "__main__":
    create_comparisons_line_chart()
    print("Algorithm comparison count chart generated successfully!") 