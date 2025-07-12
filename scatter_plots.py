import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from preprocess_data import load_data, get_algorithm_color, save_plot

def create_scatter_plots():
    """Create scatter plots with trendlines to show individual data points and performance trends."""
    # Load the preprocessed data
    _, df_long = load_data()
    
    # Create a scatter plot for execution time vs text length with trendlines
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Get unique algorithms
    algorithms = sorted(df_long['algorithm'].unique())
    
    # Plot each algorithm with a different color and add trendline
    for alg in algorithms:
        data = df_long[df_long['algorithm'] == alg]
        
        # Plot scatter points
        ax.scatter(
            data['text_length'], 
            data['execution_time'],
            alpha=0.5,
            label=alg,
            color=get_algorithm_color(alg)
        )
        
        # Fit a linear regression line
        X = data['text_length'].values.reshape(-1, 1)
        y = data['execution_time'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Create prediction line
        x_pred = np.array([min(data['text_length']), max(data['text_length'])]).reshape(-1, 1)
        y_pred = model.predict(x_pred)
        
        # Plot trendline
        ax.plot(
            x_pred, y_pred, 
            color=get_algorithm_color(alg),
            linestyle='--',
            linewidth=2
        )
    
    ax.set_xlabel('Text Length (characters)')
    ax.set_ylabel('Execution Time (seconds)')
    ax.set_title('Execution Time vs. Text Length with Trendlines')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    save_plot(fig, 'scatter_execution_time_trendline.png')
    
    # Create a scatter plot for comparisons vs text length with trendlines
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot each algorithm with a different color and add trendline
    for alg in algorithms:
        data = df_long[df_long['algorithm'] == alg]
        
        # Plot scatter points
        ax.scatter(
            data['text_length'], 
            data['comparisons'],
            alpha=0.5,
            label=alg,
            color=get_algorithm_color(alg)
        )
        
        # Fit a linear regression line
        X = data['text_length'].values.reshape(-1, 1)
        y = data['comparisons'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Create prediction line
        x_pred = np.array([min(data['text_length']), max(data['text_length'])]).reshape(-1, 1)
        y_pred = model.predict(x_pred)
        
        # Plot trendline
        ax.plot(
            x_pred, y_pred, 
            color=get_algorithm_color(alg),
            linestyle='--',
            linewidth=2
        )
    
    ax.set_xlabel('Text Length (characters)')
    ax.set_ylabel('Number of Comparisons')
    ax.set_title('Number of Comparisons vs. Text Length with Trendlines')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    save_plot(fig, 'scatter_comparisons_trendline.png')
    
    # Create a scatter plot showing the relationship between execution time and comparisons
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot each algorithm with a different color
    for alg in algorithms:
        data = df_long[df_long['algorithm'] == alg]
        
        ax.scatter(
            data['comparisons'], 
            data['execution_time'],
            alpha=0.6,
            label=alg,
            color=get_algorithm_color(alg)
        )
        
        # Add a best-fit line
        sns.regplot(
            x=data['comparisons'],
            y=data['execution_time'],
            scatter=False,
            ax=ax,
            color=get_algorithm_color(alg),
            line_kws={'linestyle': '--'}
        )
    
    ax.set_xlabel('Number of Comparisons')
    ax.set_ylabel('Execution Time (seconds)')
    ax.set_title('Execution Time vs. Number of Comparisons')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    save_plot(fig, 'scatter_time_vs_comparisons.png')

if __name__ == "__main__":
    create_scatter_plots()
    print("Scatter plots with trendlines generated successfully!") 