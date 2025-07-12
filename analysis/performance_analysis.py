import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
df = pd.read_csv('e_simulation_results.csv')

# Ensure text_length is treated as numeric
df['text_length'] = pd.to_numeric(df['text_length'])

# Create categories for text lengths
def categorize_length(length):
    if length <= 10000:
        return "10K"
    elif length <= 50000:
        return "50K"
    else:
        return "100K"

df['length_category'] = df['text_length'].apply(categorize_length)

# Filter for longer texts to better demonstrate KMP's advantages
long_texts_df = df[df['text_length'] >= 50000].copy()

# Prepare data for box plots - longer texts only
runtime_data = {
    'Naive (Stream)': long_texts_df['naive_stream_time_sec'],
    'KMP (Stream)': long_texts_df['kmp_stream_time_sec'],
    'Naive (Normal)': long_texts_df['naive_normal_time_sec'],
    'KMP (Normal)': long_texts_df['kmp_normal_time_sec']
}

# Create a figure for the box plot
plt.figure(figsize=(12, 8))
sns.set(style="whitegrid")

# Create box plot
box_plot = sns.boxplot(data=runtime_data, palette="Set3")
plt.title('Runtime Comparison: Naive vs KMP (Texts ≥ 50,000 chars)', fontsize=16)
plt.ylabel('Time (seconds)', fontsize=14)
plt.xlabel('Algorithm', fontsize=14)
plt.xticks(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Add a horizontal line for the median of KMP stream as reference
kmp_stream_median = long_texts_df['kmp_stream_time_sec'].median()
plt.axhline(y=kmp_stream_median, color='r', linestyle='--', alpha=0.5)
plt.text(3.1, kmp_stream_median, f'KMP Stream Median: {kmp_stream_median:.4f}s', 
         verticalalignment='bottom', horizontalalignment='left', color='red', fontsize=10)

# Save the plot
plt.tight_layout()
plt.savefig('kmp_vs_naive_boxplot_long_texts.png', dpi=300)

# Additionally, analyze the speedup ratios by text length categories
plt.figure(figsize=(12, 8))

# Group by length category and calculate mean speedup
speedup_by_length = df.groupby('length_category')[['kmp_vs_naive_stream_speedup_time', 
                                                 'kmp_normal_vs_naive_normal_speedup_time']].mean()

# Rename for clarity
speedup_by_length.columns = ['KMP vs Naive (Stream)', 'KMP vs Naive (Normal)']

# Plot the speedup ratios by text length
speedup_by_length.plot(kind='bar', figsize=(10, 6))
plt.title('Average Speedup Ratio: KMP vs Naive by Text Length', fontsize=16)
plt.ylabel('Speedup (Naive Time / KMP Time)', fontsize=14)
plt.xlabel('Text Length Category', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.axhline(y=1, color='red', linestyle='--')  # Add reference line at speedup=1
plt.xticks(rotation=0, fontsize=12)
plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig('kmp_vs_naive_speedup_by_length.png', dpi=300)

# Also analyze the comparison reduction by text length categories
plt.figure(figsize=(12, 8))

# Group by length category and calculate mean comparison reduction
comp_reduction_by_length = df.groupby('length_category')[['kmp_vs_naive_stream_reduction_comps', 
                                                        'kmp_normal_vs_naive_normal_reduction_comps']].mean()

# Rename for clarity
comp_reduction_by_length.columns = ['KMP vs Naive (Stream)', 'KMP vs Naive (Normal)']

# Plot the comparison reduction ratios by text length
comp_reduction_by_length.plot(kind='bar', figsize=(10, 6))
plt.title('Average Comparison Reduction: KMP vs Naive by Text Length', fontsize=16)
plt.ylabel('Reduction Ratio (Naive Comps / KMP Comps)', fontsize=14)
plt.xlabel('Text Length Category', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.axhline(y=1, color='red', linestyle='--')  # Add reference line at reduction=1
plt.xticks(rotation=0, fontsize=12)
plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig('kmp_vs_naive_comparison_reduction_by_length.png', dpi=300)

# Print summary statistics
print("SUMMARY STATISTICS FOR LONGER TEXTS (≥ 50K chars):")
print("\nMedian Runtime (seconds):")
for algo, times in runtime_data.items():
    print(f"{algo}: {times.median():.6f}")

print("\nMean Runtime (seconds):")
for algo, times in runtime_data.items():
    print(f"{algo}: {times.mean():.6f}")

print("\nMean Speedup Ratios by Text Length Category:")
print(speedup_by_length)

print("\nMean Comparison Reduction Ratios by Text Length Category:")
print(comp_reduction_by_length)

# Create another boxplot that specifically shows the speedup ratios
speedup_data = {
    'Stream (50K)': df[(df['text_length'] == 50000)]['kmp_vs_naive_stream_speedup_time'],
    'Normal (50K)': df[(df['text_length'] == 50000)]['kmp_normal_vs_naive_normal_speedup_time'],
    'Stream (100K)': df[(df['text_length'] == 100000)]['kmp_vs_naive_stream_speedup_time'],
    'Normal (100K)': df[(df['text_length'] == 100000)]['kmp_normal_vs_naive_normal_speedup_time']
}

plt.figure(figsize=(12, 8))
sns.boxplot(data=speedup_data, palette="Set2")
plt.axhline(y=1, color='r', linestyle='--', alpha=0.7)
plt.title('KMP vs Naive Speedup Ratios by Text Length', fontsize=16)
plt.ylabel('Speedup Ratio (Naive Time / KMP Time)', fontsize=14)
plt.xlabel('Algorithm Type and Text Length', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('kmp_vs_naive_speedup_boxplot.png', dpi=300) 