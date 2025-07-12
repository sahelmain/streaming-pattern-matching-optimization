import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from preprocess_data import load_data, save_plot

def create_heatmaps():
    """Create heatmaps to show performance across multiple dimensions."""
    # Load the original data (not the long format)
    df, _ = load_data()
    
    # Create a heatmap of KMP stream speedup by pattern_ip and text_ip
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Pivot the data to create a matrix for the heatmap
    pivot_df = df.pivot_table(
        index='pattern_ip',
        columns='text_ip',
        values='kmp_vs_naive_stream_speedup_time',
        aggfunc='mean'
    )
    
    # Create the heatmap
    sns.heatmap(pivot_df, annot=True, fmt=".2f", cmap="YlGnBu", ax=ax, 
                cbar_kws={'label': 'KMP vs Naive Stream Speedup'})
    
    ax.set_title('KMP vs Naive Stream Speedup by Pattern IP and Text IP')
    ax.set_xlabel('Text IP')
    ax.set_ylabel('Pattern IP')
    
    save_plot(fig, 'heatmap_speedup_by_ip.png')
    
    # Create a heatmap of comparison reduction by text length and pattern IP
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create a new pivot table for comparison reduction
    pivot_comp = df.pivot_table(
        index='pattern_ip',
        columns='text_length',
        values='kmp_vs_naive_stream_reduction_comps',
        aggfunc='mean'
    )
    
    # Create the heatmap
    sns.heatmap(pivot_comp, annot=True, fmt=".2f", cmap="YlOrRd", ax=ax,
                cbar_kws={'label': 'KMP vs Naive Stream Comparison Reduction'})
    
    ax.set_title('KMP vs Naive Stream Comparison Reduction by Pattern IP and Text Length')
    ax.set_xlabel('Text Length')
    ax.set_ylabel('Pattern IP')
    
    save_plot(fig, 'heatmap_reduction_by_length.png')
    
    # Create a heatmap of execution time for all algorithms by text length
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Prepare data for this heatmap
    # Group by algorithm and text_length to calculate mean execution time
    time_cols = [
        'naive_stream_time_sec', 
        'kmp_stream_time_sec',
        'naive_normal_time_sec',
        'kmp_normal_time_sec'
    ]
    
    # Create a new dataframe for the execution time heatmap
    time_data = []
    
    for text_len in sorted(df['text_length'].unique()):
        df_subset = df[df['text_length'] == text_len]
        row = {'text_length': text_len}
        
        for col in time_cols:
            alg_name = col.replace('_time_sec', '')
            row[alg_name] = df_subset[col].mean()
            
        time_data.append(row)
    
    time_df = pd.DataFrame(time_data)
    time_df = time_df.set_index('text_length')
    
    # Rename columns for better labels
    time_df.columns = ['Naive Stream', 'KMP Stream', 'Naive Normal', 'KMP Normal']
    
    # Create the heatmap
    sns.heatmap(time_df, annot=True, fmt=".4f", cmap="viridis", ax=ax,
                cbar_kws={'label': 'Execution Time (seconds)'})
    
    ax.set_title('Mean Execution Time by Algorithm and Text Length')
    ax.set_xlabel('Algorithm')
    ax.set_ylabel('Text Length')
    
    save_plot(fig, 'heatmap_execution_time.png')

if __name__ == "__main__":
    create_heatmaps()
    print("Heatmaps generated successfully!") 