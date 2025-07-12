import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
df = pd.read_csv('../e_simulation_results.csv')

# Ensure text_length is treated as numeric
df['text_length'] = pd.to_numeric(df['text_length'])

# Create a figure for the overall comparison (all texts)
plt.figure(figsize=(12, 7))
algo_columns = ['naive_stream_time_sec', 'kmp_stream_time_sec', 'naive_normal_time_sec', 'kmp_normal_time_sec']
algo_labels = ['Naive Stream', 'KMP Stream', 'Naive Normal', 'KMP Normal']

# Create the boxplot for all text lengths
ax = sns.boxplot(data=df[algo_columns])
plt.title('Algorithm Execution Time Comparison - All Text Lengths (Chunk Size 1)', fontsize=16)
plt.ylabel('Time (seconds)', fontsize=14)
plt.xlabel('Algorithm', fontsize=14)
plt.xticks(range(len(algo_labels)), algo_labels, fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('algorithm_comparison_all_texts.png', dpi=300)
plt.close()

# Create separate boxplots for each text length
text_lengths = sorted(df['text_length'].unique())

# Create a visualization for each text length
for length in text_lengths:
    subset = df[df['text_length'] == length]
    
    plt.figure(figsize=(12, 7))
    sns.boxplot(data=subset[algo_columns])
    plt.title(f'Algorithm Execution Time - {length} Character Texts (Chunk Size 1)', fontsize=16)
    plt.ylabel('Time (seconds)', fontsize=14)
    plt.xlabel('Algorithm', fontsize=14)
    plt.xticks(range(len(algo_labels)), algo_labels, fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f'algorithm_comparison_{length}_chars.png', dpi=300)
    plt.close()

# Calculate summary statistics for each algorithm by text length
summary_stats = []

for length in text_lengths:
    subset = df[df['text_length'] == length]
    
    row = {'Text Length': length}
    for i, col in enumerate(algo_columns):
        row[f'{algo_labels[i]} Mean (s)'] = subset[col].mean()
        row[f'{algo_labels[i]} Median (s)'] = subset[col].median()
    
    # Add speedup ratios
    row['KMP vs Naive Stream Speedup'] = subset['kmp_vs_naive_stream_speedup_time'].mean()
    row['KMP vs Naive Normal Speedup'] = subset['kmp_normal_vs_naive_normal_speedup_time'].mean()
    
    summary_stats.append(row)

# Convert to DataFrame and print
summary_df = pd.DataFrame(summary_stats)
print("\nSummary Statistics by Text Length:")
print(summary_df.to_string(index=False, float_format=lambda x: f"{x:.6f}"))

# Create a bar chart showing mean execution times by text length
plt.figure(figsize=(14, 8))

bar_width = 0.2
x = np.arange(len(text_lengths))

for i, col in enumerate(algo_columns):
    means = [df[df['text_length'] == length][col].mean() for length in text_lengths]
    plt.bar(x + i*bar_width, means, width=bar_width, label=algo_labels[i])

plt.title('Mean Algorithm Execution Time by Text Length (Chunk Size 1)', fontsize=16)
plt.ylabel('Time (seconds)', fontsize=14)
plt.xlabel('Text Length', fontsize=14)
plt.xticks(x + bar_width*1.5, text_lengths, fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7, axis='y')
plt.tight_layout()
plt.savefig('mean_execution_time_by_length.png', dpi=300)
plt.close()

# Create violin plots to better visualize the distribution
plt.figure(figsize=(14, 8))

# Prepare data for violin plot
df_melted = pd.melt(df, 
                   id_vars=['text_length'], 
                   value_vars=algo_columns,
                   var_name='Algorithm', value_name='Time (seconds)')

# Map algorithm names to more readable versions
df_melted['Algorithm'] = df_melted['Algorithm'].map(dict(zip(algo_columns, algo_labels)))
df_melted['Text Length'] = df_melted['text_length'].astype(str)

# Create violin plot
sns.violinplot(x='Algorithm', y='Time (seconds)', hue='Text Length', data=df_melted, split=True)
plt.title('Algorithm Execution Time Distribution by Text Length (Chunk Size 1)', fontsize=16)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Text Length', fontsize=12)
plt.tight_layout()
plt.savefig('execution_time_violin_plot.png', dpi=300)
plt.close()

# Create comparison count analysis
plt.figure(figsize=(14, 8))
comp_columns = ['naive_stream_comparisons', 'kmp_stream_comparisons', 
                'naive_normal_comparisons', 'kmp_normal_comparisons']
comp_labels = ['Naive Stream', 'KMP Stream', 'Naive Normal', 'KMP Normal']

# Calculate means for each text length
comp_means = []
for length in text_lengths:
    subset = df[df['text_length'] == length]
    comp_means.append([subset[col].mean() for col in comp_columns])

# Plot the comparison counts
x = np.arange(len(text_lengths))
bar_width = 0.2

for i in range(len(comp_columns)):
    heights = [comp_means[j][i] for j in range(len(text_lengths))]
    plt.bar(x + i*bar_width, heights, width=bar_width, label=comp_labels[i])

plt.title('Mean Comparison Count by Algorithm and Text Length (Chunk Size 1)', fontsize=16)
plt.ylabel('Number of Comparisons', fontsize=14)
plt.xlabel('Text Length', fontsize=14)
plt.xticks(x + bar_width*1.5, text_lengths, fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7, axis='y')
plt.tight_layout()
plt.savefig('mean_comparison_count_by_length.png', dpi=300)
plt.close()

# Save the summary statistics to CSV for future reference
summary_df.to_csv('algorithm_performance_summary.csv', index=False)

print("\nAnalysis complete! All visualizations have been generated.") 