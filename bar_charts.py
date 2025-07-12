import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from preprocess_data import load_data, get_algorithm_color, save_plot

def create_bar_charts():
    """Create bar charts with error bars for algorithm comparison."""
    # Load the preprocessed data
    _, df_long = load_data()
    
    # Create a figure for execution time comparison
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Group by algorithm and text size, then calculate mean and std
    grouped = df_long.groupby(['algorithm', 'text_size_category'])['execution_time'].agg(['mean', 'std']).reset_index()
    
    # Plot the bar chart with error bars
    bar_width = 0.2
    text_sizes = sorted(df_long['text_size_category'].unique())
    algorithms = sorted(df_long['algorithm'].unique())
    
    for i, alg in enumerate(algorithms):
        data = grouped[grouped['algorithm'] == alg]
        x_pos = np.arange(len(text_sizes)) + i * bar_width - (len(algorithms)-1)*bar_width/2
        
        ax.bar(x_pos, 
               data['mean'], 
               width=bar_width, 
               yerr=data['std'],
               label=alg,
               color=get_algorithm_color(alg),
               capsize=5)
    
    ax.set_xticks(np.arange(len(text_sizes)))
    ax.set_xticklabels(text_sizes)
    ax.set_ylabel('Execution Time (seconds)')
    ax.set_xlabel('Text Size')
    ax.set_title('Mean Execution Time by Algorithm and Text Size')
    ax.legend()
    
    save_plot(fig, 'bar_chart_execution_time.png')
    
    # Create a figure for comparison counts
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Group by algorithm and text size, then calculate mean and std for comparisons
    grouped = df_long.groupby(['algorithm', 'text_size_category'])['comparisons'].agg(['mean', 'std']).reset_index()
    
    # Plot the bar chart with error bars
    for i, alg in enumerate(algorithms):
        data = grouped[grouped['algorithm'] == alg]
        x_pos = np.arange(len(text_sizes)) + i * bar_width - (len(algorithms)-1)*bar_width/2
        
        ax.bar(x_pos, 
               data['mean'], 
               width=bar_width, 
               yerr=data['std'],
               label=alg,
               color=get_algorithm_color(alg),
               capsize=5)
    
    ax.set_xticks(np.arange(len(text_sizes)))
    ax.set_xticklabels(text_sizes)
    ax.set_ylabel('Number of Comparisons')
    ax.set_xlabel('Text Size')
    ax.set_title('Mean Comparison Count by Algorithm and Text Size')
    ax.legend()
    
    save_plot(fig, 'bar_chart_comparisons.png')
    
    # Create a bar chart for speedup ratio
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Use the original dataframe to calculate algorithm speedups
    df, _ = load_data()
    
    # Add text size category label to speedup data
    speedup_df = df[['text_size_category', 'kmp_vs_naive_stream_speedup_time', 
                    'kmp_normal_vs_naive_normal_speedup_time']].copy()
    
    # Calculate average speedup by text size
    grouped_speedup = speedup_df.groupby('text_size_category').agg({
        'kmp_vs_naive_stream_speedup_time': ['mean', 'std'],
        'kmp_normal_vs_naive_normal_speedup_time': ['mean', 'std']
    }).reset_index()
    
    # Flatten multi-level columns
    grouped_speedup.columns = ['text_size_category', 
                              'stream_speedup_mean', 'stream_speedup_std', 
                              'normal_speedup_mean', 'normal_speedup_std']
    
    # Plot the speedup bar chart
    x_pos = np.arange(len(text_sizes))
    bar_width = 0.35
    
    ax.bar(x_pos - bar_width/2, 
           grouped_speedup['stream_speedup_mean'], 
           width=bar_width, 
           yerr=grouped_speedup['stream_speedup_std'],
           label='KMP vs Naive (Stream)',
           color='blue',
           capsize=5)
    
    ax.bar(x_pos + bar_width/2, 
           grouped_speedup['normal_speedup_mean'], 
           width=bar_width, 
           yerr=grouped_speedup['normal_speedup_std'],
           label='KMP vs Naive (Normal)',
           color='green',
           capsize=5)
    
    ax.axhline(y=1.0, color='red', linestyle='--', label='Equal Performance')
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels(text_sizes)
    ax.set_ylabel('Speedup Ratio')
    ax.set_xlabel('Text Size')
    ax.set_title('KMP Speedup Ratio Compared to Naive Algorithms')
    ax.legend()
    
    save_plot(fig, 'bar_chart_speedup_ratio.png')

if __name__ == "__main__":
    create_bar_charts()
    print("Bar charts with error bars generated successfully!") 