import os
import time
from preprocess_data import load_data
from bar_charts import create_bar_charts
from line_charts import create_line_charts
from log_scale_plots import create_log_scale_plots
from heatmaps import create_heatmaps
from violin_plots import create_violin_plots
from scatter_plots import create_scatter_plots

def main():
    """Generate all visualization types."""
    # Create output directory if it doesn't exist
    output_dir = "visualizations"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    # Change working directory to output directory
    os.chdir(output_dir)
    
    start_time = time.time()
    
    # Preprocess data
    print("Preprocessing data...")
    df, df_long = load_data()
    print(f"Loaded data with {len(df)} original rows, {len(df_long)} rows in long format")
    
    # Generate all visualization types
    print("\nGenerating bar charts...")
    create_bar_charts()
    
    print("\nGenerating line charts...")
    create_line_charts()
    
    print("\nGenerating log-scale plots...")
    create_log_scale_plots()
    
    print("\nGenerating heatmaps...")
    create_heatmaps()
    
    print("\nGenerating violin plots...")
    create_violin_plots()
    
    print("\nGenerating scatter plots with trendlines...")
    create_scatter_plots()
    
    end_time = time.time()
    
    print(f"\nAll visualizations generated successfully in {end_time - start_time:.2f} seconds!")
    print(f"Visualizations saved to: {os.getcwd()}")

if __name__ == "__main__":
    main() 