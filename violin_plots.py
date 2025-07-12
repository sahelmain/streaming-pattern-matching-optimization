import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from preprocess_data import load_data, save_plot

def create_violin_plots():
    """Create violin plots to show distribution shapes better than boxplots."""
    # Load the preprocessed data in long format
    _, df_long = load_data()
    
    # Create a violin plot for execution time by algorithm and text size
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create the violin plot
    sns.violinplot(
        data=df_long,
        x='text_size_category',
        y='execution_time',
        hue='algorithm',
        split=False,
        inner='quartile',
        ax=ax
    )
    
    ax.set_title('Distribution of Execution Time by Algorithm and Text Size')
    ax.set_xlabel('Text Size')
    ax.set_ylabel('Execution Time (seconds)')
    ax.legend(title='Algorithm')
    
    save_plot(fig, 'violin_execution_time.png')
    
    # Create a violin plot for comparison counts
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create the violin plot for small/medium text only (large values skew the plot)
    small_medium_df = df_long[df_long['text_size_category'] != 'Large (100K)']
    
    sns.violinplot(
        data=small_medium_df,
        x='text_size_category',
        y='comparisons',
        hue='algorithm',
        split=False,
        inner='quartile',
        ax=ax
    )
    
    ax.set_title('Distribution of Comparison Counts by Algorithm (Small & Medium Text Sizes)')
    ax.set_xlabel('Text Size')
    ax.set_ylabel('Number of Comparisons')
    ax.legend(title='Algorithm')
    
    save_plot(fig, 'violin_comparisons_small_medium.png')
    
    # Create a log-scale violin plot for comparison counts including all data
    fig, ax = plt.subplots(figsize=(12, 8))
    
    sns.violinplot(
        data=df_long,
        x='text_size_category',
        y='comparisons',
        hue='algorithm',
        split=False,
        inner='quartile',
        ax=ax
    )
    
    ax.set_yscale('log')
    ax.set_title('Distribution of Comparison Counts by Algorithm (Log Scale)')
    ax.set_xlabel('Text Size')
    ax.set_ylabel('Number of Comparisons (log scale)')
    ax.legend(title='Algorithm')
    
    save_plot(fig, 'violin_comparisons_log_scale.png')
    
    # Create a violin plot for speedup ratio
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Use the original dataframe for speedup ratios
    df, _ = load_data()
    
    # Prepare data for the speedup violin plot
    speedup_data = []
    
    # KMP vs Naive Stream
    kmp_stream_df = df[['text_size_category', 'kmp_vs_naive_stream_speedup_time']].copy()
    kmp_stream_df['comparison_type'] = 'KMP vs Naive (Stream)'
    kmp_stream_df = kmp_stream_df.rename(columns={'kmp_vs_naive_stream_speedup_time': 'speedup'})
    
    # KMP vs Naive Normal
    kmp_normal_df = df[['text_size_category', 'kmp_normal_vs_naive_normal_speedup_time']].copy()
    kmp_normal_df['comparison_type'] = 'KMP vs Naive (Normal)'
    kmp_normal_df = kmp_normal_df.rename(columns={'kmp_normal_vs_naive_normal_speedup_time': 'speedup'})
    
    speedup_data = pd.concat([kmp_stream_df, kmp_normal_df], ignore_index=True)
    
    # Create the violin plot for speedup
    sns.violinplot(
        data=speedup_data,
        x='text_size_category',
        y='speedup',
        hue='comparison_type',
        split=True,
        inner='quartile',
        ax=ax
    )
    
    ax.axhline(y=1.0, color='red', linestyle='--', label='Equal Performance')
    ax.set_title('Distribution of KMP Speedup Ratio by Text Size')
    ax.set_xlabel('Text Size')
    ax.set_ylabel('Speedup Ratio')
    ax.legend(title='Comparison Type')
    
    save_plot(fig, 'violin_speedup_ratio.png')

if __name__ == "__main__":
    create_violin_plots()
    print("Violin plots generated successfully!") 