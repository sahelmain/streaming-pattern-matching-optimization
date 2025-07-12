import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from preprocess_data import load_data, get_algorithm_color, save_plot

def create_log_scale_plots():
    """Create log-scale plots for better visualization of data with wide value ranges."""
    # Load the preprocessed data
    _, df_long = load_data()
    
    # Create a log-scale plot for comparisons
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Calculate mean comparisons for each algorithm and text length
    grouped = df_long.groupby(['algorithm', 'text_length'])['comparisons'].mean().reset_index()
    
    # Plot lines for each algorithm on log scale
    algorithms = sorted(df_long['algorithm'].unique())
    for alg in algorithms:
        data = grouped[grouped['algorithm'] == alg]
        ax.plot(data['text_length'], data['comparisons'], 
                marker='o', label=alg, color=get_algorithm_color(alg))
    
    ax.set_yscale('log')
    ax.set_xlabel('Text Length (characters)')
    ax.set_ylabel('Number of Comparisons (log scale)')
    ax.set_title('Number of Comparisons vs. Text Length (Log Scale)')
    ax.legend()
    ax.grid(True, which="both", ls="--")
    
    save_plot(fig, 'log_scale_comparisons.png')
    
    # Create a log-log plot to visualize the scaling behavior
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for alg in algorithms:
        data = grouped[grouped['algorithm'] == alg]
        ax.loglog(data['text_length'], data['comparisons'], 
                marker='o', label=alg, color=get_algorithm_color(alg))
    
    ax.set_xlabel('Text Length (log scale)')
    ax.set_ylabel('Number of Comparisons (log scale)')
    ax.set_title('Scaling Behavior: Log-Log Plot of Comparisons vs. Text Length')
    ax.legend()
    ax.grid(True, which="both", ls="--")
    
    save_plot(fig, 'log_log_comparisons.png')
    
    # Create a log-scale ratio plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Use the original dataframe for comparison reduction ratios
    df, _ = load_data()
    
    # Calculate average comparison reduction by text length
    reduction_df = df.groupby('text_length').agg({
        'kmp_vs_naive_stream_reduction_comps': 'mean',
        'kmp_normal_vs_naive_normal_reduction_comps': 'mean',
    }).reset_index()
    
    # Plot the reduction ratio on log scale
    ax.semilogy(reduction_df['text_length'], 
                reduction_df['kmp_vs_naive_stream_reduction_comps'], 
                marker='o', label='KMP vs Naive (Stream)', color='blue')
    
    ax.semilogy(reduction_df['text_length'], 
                reduction_df['kmp_normal_vs_naive_normal_reduction_comps'], 
                marker='s', label='KMP vs Naive (Normal)', color='green')
    
    ax.axhline(y=1.0, color='red', linestyle='--', label='Equal Comparisons')
    
    ax.set_xlabel('Text Length (characters)')
    ax.set_ylabel('Comparison Reduction Ratio (log scale)')
    ax.set_title('KMP Comparison Reduction Ratio vs. Text Length')
    ax.legend()
    ax.grid(True, which="both", ls="--")
    
    save_plot(fig, 'log_scale_reduction_ratio.png')

if __name__ == "__main__":
    create_log_scale_plots()
    print("Log-scale plots generated successfully!") 