import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from preprocess_data import load_data, save_plot

def create_algorithm_comparison_by_pattern():
    """Create a line chart showing time complexity comparison between the 4 algorithms by pattern length."""
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
    
    # Get unique pattern lengths from the data
    pattern_ips = sorted(df['pattern_ip'].unique())
    
    # For each text length, we'll create a separate line chart
    text_lengths = [10000, 50000, 100000]
    
    # We'll create one plot with three subplots (one for each text length)
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
    
    for i, text_len in enumerate(text_lengths):
        # Filter data for this text length
        df_text = df[df['text_length'] == text_len]
        
        # Group by pattern_ip
        grouped = df_text.groupby('pattern_ip').agg({
            'naive_stream_time_sec': 'mean',
            'kmp_stream_time_sec': 'mean',
            'naive_normal_time_sec': 'mean',
            'kmp_normal_time_sec': 'mean',
            'pattern_length': 'first'  # Get the pattern length for each pattern_ip
        }).reset_index()
        
        # Sort by pattern_ip
        grouped = grouped.sort_values('pattern_ip')
        
        # Plot each algorithm on this subplot
        for alg, color in colors.items():
            # Convert algorithm name to a more readable format for the legend
            alg_label = alg.replace('_time_sec', '').replace('_', ' ').title()
            
            axes[i].plot(
                grouped['pattern_ip'],
                grouped[alg],
                label=alg_label if i == 0 else "",  # Only show legend on first subplot
                color=color,
                marker='o',
                markersize=6,
                linewidth=2
            )
        
        # Set title for this subplot
        axes[i].set_title(f'Text Length: {text_len}', fontsize=14)
        axes[i].set_xlabel('Pattern IP', fontsize=12)
        
        # Set x-ticks to pattern IPs
        axes[i].set_xticks(pattern_ips)
        
        # Add grid to this subplot
        axes[i].grid(True, linestyle='--', alpha=0.7)
    
    # Add a common y label
    fig.text(0.04, 0.5, 'Execution Time (s)', va='center', rotation='vertical', fontsize=14)
    
    # Add a common title
    plt.suptitle('Algorithm Performance by Pattern Type and Text Length', fontsize=16)
    
    # Add legend to the figure
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.05), ncol=4, fontsize=12)
    
    # Add some spacing for the legend
    plt.tight_layout(rect=[0, 0.07, 1, 0.96])
    
    # Save the plot
    save_plot(fig, 'algorithm_by_pattern_comparison.png')

if __name__ == "__main__":
    create_algorithm_comparison_by_pattern()
    print("Algorithm performance by pattern comparison generated successfully!") 