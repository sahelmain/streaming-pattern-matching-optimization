import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
df = pd.read_csv('../e_simulation_results.csv')

# The user's original code
plt.figure(figsize=(10,6))
sns.boxplot(data=df[['naive_stream_time_sec', 'kmp_stream_time_sec', 'naive_normal_time_sec', 'kmp_normal_time_sec']])
plt.ylabel('Time (seconds)')
plt.title('Algorithm Execution Time Comparison - All Text Lengths (Original)')
plt.savefig('original_boxplot.png')
plt.close()

# Create length categories
df['length_category'] = pd.cut(df['text_length'], 
                              bins=[0, 10000, 50000, 100000, float('inf')],
                              labels=['10K', '50K', '100K', '>100K'])

# Show the distribution of text lengths in the dataset
length_counts = df['text_length'].value_counts().sort_index()
print("Distribution of text lengths in the dataset:")
print(length_counts)

print("\nCount by length category:")
print(df['length_category'].value_counts())

# Problem 1: Distribution bias - more short text samples where naive looks better
plt.figure(figsize=(8, 5))
df['length_category'].value_counts().sort_index().plot(kind='bar')
plt.title('Number of Samples by Text Length Category')
plt.xlabel('Text Length')
plt.ylabel('Count')
plt.savefig('length_distribution.png')
plt.close()

# Problem 2: KMP's extreme outliers on short texts can distort the overall boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(x='length_category', y='kmp_stream_time_sec', data=df)
plt.title('KMP Stream Runtime by Text Length')
plt.xlabel('Text Length')
plt.ylabel('Time (seconds)')
plt.savefig('kmp_by_length.png')
plt.close()

# Problem 3: Skewed overall mean due to dominance of short texts
means = {
    'Runtime (All Lengths)': {
        'Naive Stream': df['naive_stream_time_sec'].mean(),
        'KMP Stream': df['kmp_stream_time_sec'].mean(),
        'Naive Normal': df['naive_normal_time_sec'].mean(),
        'KMP Normal': df['kmp_normal_time_sec'].mean()
    },
    'Runtime (10K texts only)': {
        'Naive Stream': df[df['text_length'] == 10000]['naive_stream_time_sec'].mean(),
        'KMP Stream': df[df['text_length'] == 10000]['kmp_stream_time_sec'].mean(),
        'Naive Normal': df[df['text_length'] == 10000]['naive_normal_time_sec'].mean(),
        'KMP Normal': df[df['text_length'] == 10000]['kmp_normal_time_sec'].mean()
    },
    'Runtime (50K texts only)': {
        'Naive Stream': df[df['text_length'] == 50000]['naive_stream_time_sec'].mean(),
        'KMP Stream': df[df['text_length'] == 50000]['kmp_stream_time_sec'].mean(),
        'Naive Normal': df[df['text_length'] == 50000]['naive_normal_time_sec'].mean(),
        'KMP Normal': df[df['text_length'] == 50000]['kmp_normal_time_sec'].mean()
    },
    'Runtime (100K texts only)': {
        'Naive Stream': df[df['text_length'] == 100000]['naive_stream_time_sec'].mean(),
        'KMP Stream': df[df['text_length'] == 100000]['kmp_stream_time_sec'].mean(),
        'Naive Normal': df[df['text_length'] == 100000]['naive_normal_time_sec'].mean(),
        'KMP Normal': df[df['text_length'] == 100000]['kmp_normal_time_sec'].mean()
    }
}

print("\nMean Execution Times:")
for category, algos in means.items():
    print(f"\n{category}")
    for algo, mean_time in algos.items():
        print(f"{algo}: {mean_time:.6f} seconds")

# Better Approach 1: Split boxplots by text length
plt.figure(figsize=(12, 8))
df_melted = pd.melt(df, 
                    id_vars=['length_category'], 
                    value_vars=['naive_stream_time_sec', 'kmp_stream_time_sec', 
                              'naive_normal_time_sec', 'kmp_normal_time_sec'],
                    var_name='Algorithm', value_name='Time (seconds)')

# Rename algorithm names for better readability
algo_names = {
    'naive_stream_time_sec': 'Naive (Stream)',
    'kmp_stream_time_sec': 'KMP (Stream)',
    'naive_normal_time_sec': 'Naive (Normal)',
    'kmp_normal_time_sec': 'KMP (Normal)'
}
df_melted['Algorithm'] = df_melted['Algorithm'].map(algo_names)

# Create faceted boxplots by text length
sns.boxplot(x='Algorithm', y='Time (seconds)', hue='length_category', data=df_melted)
plt.title('Algorithm Execution Time by Text Length Categories')
plt.legend(title='Text Length')
plt.savefig('faceted_boxplot.png')
plt.close()

# Better Approach 2: Show only longer texts where KMP's advantage is evident
plt.figure(figsize=(10, 6))
long_texts = df[df['text_length'] >= 50000]
sns.boxplot(data=long_texts[['naive_stream_time_sec', 'kmp_stream_time_sec', 
                           'naive_normal_time_sec', 'kmp_normal_time_sec']])
plt.title('Algorithm Execution Time - Long Texts Only (≥50K)')
plt.ylabel('Time (seconds)')
plt.xticks(range(4), ['Naive (Stream)', 'KMP (Stream)', 'Naive (Normal)', 'KMP (Normal)'])
plt.savefig('long_texts_boxplot.png')
plt.close()

# Better Approach 3: Stratified speedup ratios
plt.figure(figsize=(10, 6))
speedup_df = pd.DataFrame({
    '10K': df[df['text_length'] == 10000]['kmp_vs_naive_stream_speedup_time'],
    '50K': df[df['text_length'] == 50000]['kmp_vs_naive_stream_speedup_time'],
    '100K': df[df['text_length'] == 100000]['kmp_vs_naive_stream_speedup_time']
})
sns.boxplot(data=speedup_df)
plt.axhline(y=1, color='r', linestyle='--')
plt.title('KMP vs Naive Speedup Ratio by Text Length (Stream)')
plt.ylabel('Speedup Ratio (Naive Time / KMP Time)')
plt.xlabel('Text Length')
plt.savefig('speedup_by_length_boxplot.png')
plt.close()

print("\nDone! All visualization files have been created. Check the PNG files to understand why the original boxplot might be misleading.") 