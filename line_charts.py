import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from preprocess_data import load_data, get_algorithm_color, save_plot

def create_line_charts():
    """Create line charts to show how performance scales with input size."""
    # Load the preprocessed data
    _, df_long = load_data()
    
    # Group by algorithm and text_length for the line chart
    text_lengths = sorted(df_long['text_length'].unique())
    algorithms = sorted(df_long['algorithm'].unique())
    
    # Create a figure for execution time vs. text length
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Calculate mean execution time for each algorithm and text length
    grouped = df_long.groupby(['algorithm', 'text_length'])['execution_time'].mean().reset_index()
    
    # Plot lines for each algorithm
    for alg in algorithms:
        data = grouped[grouped['algorithm'] == alg]
        ax.plot(data['text_length'], data['execution_time'], 
                marker='o', label=alg, color=get_algorithm_color(alg))
    
    ax.set_xticks(text_lengths)
    ax.set_xlabel('Text Length (characters)')
    ax.set_ylabel('Execution Time (seconds)')
    ax.set_title('Execution Time vs. Text Length by Algorithm')
    ax.legend()
    ax.grid(True)
    
    save_plot(fig, 'line_chart_execution_time.png')
    
    # Create a figure for comparisons vs. text length
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Calculate mean comparisons for each algorithm and text length
    grouped = df_long.groupby(['algorithm', 'text_length'])['comparisons'].mean().reset_index()
    
    # Plot lines for each algorithm
    for alg in algorithms:
        data = grouped[grouped['algorithm'] == alg]
        ax.plot(data['text_length'], data['comparisons'], 
                marker='o', label=alg, color=get_algorithm_color(alg))
    
    ax.set_xticks(text_lengths)
    ax.set_xlabel('Text Length (characters)')
    ax.set_ylabel('Number of Comparisons')
    ax.set_title('Number of Comparisons vs. Text Length by Algorithm')
    ax.legend()
    ax.grid(True)
    
    save_plot(fig, 'line_chart_comparisons.png')
    
    # Create a line chart for KMP vs Naive speedup
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Use the original dataframe to calculate algorithm speedups
    df, _ = load_data()
    
    # Calculate average speedup by text length
    speedup_df = df.groupby('text_length').agg({
        'kmp_vs_naive_stream_speedup_time': 'mean',
        'kmp_normal_vs_naive_normal_speedup_time': 'mean',
    }).reset_index()
    
    # Plot the speedup line chart
    ax.plot(speedup_df['text_length'], 
            speedup_df['kmp_vs_naive_stream_speedup_time'], 
            marker='o', label='KMP vs Naive (Stream)', color='blue')
    
    ax.plot(speedup_df['text_length'], 
            speedup_df['kmp_normal_vs_naive_normal_speedup_time'], 
            marker='s', label='KMP vs Naive (Normal)', color='green')
    
    ax.axhline(y=1.0, color='red', linestyle='--', label='Equal Performance')
    
    ax.set_xlabel('Text Length (characters)')
    ax.set_ylabel('Speedup Ratio')
    ax.set_title('KMP Speedup Ratio vs. Text Length')
    ax.legend()
    ax.grid(True)
    
    save_plot(fig, 'line_chart_speedup_ratio.png')

if __name__ == "__main__":
    create_line_charts()
    print("Line charts generated successfully!") 