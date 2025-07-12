import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import os

# Set the style for the plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_context("paper", font_scale=1.2)

# Define the custom colors for the algorithms
COLOR_NAIVE_STREAM = '#1f77b4'  # blue
COLOR_KMP_STREAM = '#ff7f0e'    # orange
COLOR_NAIVE_NORMAL = '#2ca02c'  # green
COLOR_KMP_NORMAL = '#d62728'    # red

def load_data(filepath=None):
    """Load the simulation results data."""
    # If filepath is not provided, use the default one
    if filepath is None:
        # Get the absolute path of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(current_dir, 'e_simulation_results.csv')
        
    print(f"Loading data from: {filepath}")
    df = pd.read_csv(filepath)
    
    # Create a new column for text size category
    df['text_size_category'] = pd.cut(
        df['text_length'],
        bins=[0, 15000, 75000, np.inf],
        labels=['Small (10K)', 'Medium (50K)', 'Large (100K)']
    )
    
    # Create a column with algorithm names for easier plotting
    df['algorithm'] = 'Unknown'
    df['execution_time'] = np.nan
    df['comparisons'] = np.nan
    
    # Extract data for each algorithm into long format
    algorithms = [
        ('Naive Stream', 'naive_stream_time_sec', 'naive_stream_comparisons'),
        ('KMP Stream', 'kmp_stream_time_sec', 'kmp_stream_comparisons'),
        ('Naive Normal', 'naive_normal_time_sec', 'naive_normal_comparisons'),
        ('KMP Normal', 'kmp_normal_time_sec', 'kmp_normal_comparisons')
    ]
    
    # Create a long-format dataframe for easier plotting
    dfs = []
    for alg_name, time_col, comp_col in algorithms:
        df_alg = df.copy()
        df_alg['algorithm'] = alg_name
        df_alg['execution_time'] = df_alg[time_col]
        df_alg['comparisons'] = df_alg[comp_col]
        dfs.append(df_alg)
    
    df_long = pd.concat(dfs, ignore_index=True)
    
    return df, df_long

def get_algorithm_color(algorithm):
    """Get the color for a specific algorithm."""
    color_map = {
        'Naive Stream': COLOR_NAIVE_STREAM,
        'KMP Stream': COLOR_KMP_STREAM,
        'Naive Normal': COLOR_NAIVE_NORMAL,
        'KMP Normal': COLOR_KMP_NORMAL
    }
    return color_map.get(algorithm, 'gray')

def save_plot(fig, filename, dpi=300):
    """Save the figure with proper formatting."""
    fig.tight_layout()
    plt.savefig(filename, dpi=dpi, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {filename}")

if __name__ == "__main__":
    # Load and process the data
    df, df_long = load_data()
    print(f"Loaded data with {len(df)} original rows, {len(df_long)} rows in long format")
    print("Data successfully preprocessed and ready for visualization.") 