import pandas as pd
from collections import defaultdict
import time
import csv
import os

from functions import (
    stream_data,
    naive_stream_matching_with_counts,
    kmp_stream_matching_with_counts
)

# Define these at a scope accessible by the __main__ block if used there for checks
generated_file_prefix = "flow_sequences_" # Used in main and potentially in __main__ check
target_sizes_mb = [10, 20, 30, 40, 50]     # Used in main and potentially in __main__ check


# Define known compromise dates and IPs
compromise_info = {
    1: "2006-08-24",
    5: "2006-09-04",
    4: "2006-09-18",
    3: "2006-09-26",
    6: "2006-09-26"
}
def main():
    print("Starting custom pattern matching tests with augmented flow files...")

    predefined_patterns = {
        "1": "xxxxxxx", # Pattern for IP 1
        "5": "mmmmmmm", # Pattern for IP 5
        "4": "hxxhhxx", # Pattern for IP 4
        "3": "mmmmmmm", # Pattern for IP 3
        "6": "mmmmmmh"  # Pattern for IP 6
    }
    # Add other IPs from your flow_sequences.txt if they also have patterns to test, 
    # or if you want to test these patterns against all IPs.
    # For this example, we'll only test IPs that have a predefined pattern.

    all_results = []
    header = [
        "text_file_size_mb", "target_ip", "pattern_used",
        "text_length_chars", "pattern_length_chars",
        "naive_match_count", "naive_time_sec", "naive_comparisons",
        "kmp_match_count", "kmp_time_sec", "kmp_comparisons",
        "kmp_speedup_ratio_time", "kmp_reduction_ratio_comps"
    ]

    for size_mb in target_sizes_mb:
        data_file_path = f"{generated_file_prefix}{size_mb}mb.txt"
        print(f"\n===== PROCESSING FILE: {data_file_path} =====")

        if not os.path.exists(data_file_path):
            print(f"  File '{data_file_path}' not found. Skipping.")
            continue

        ip_flow_sequences_from_file = {}
        try:
            with open(data_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        ip_str, seq_str = line.split(':', 1)
                        ip_flow_sequences_from_file[ip_str.strip()] = seq_str.strip()
                    except ValueError:
                        print(f"    Warning: Skipping malformed line in '{data_file_path}': {line}")
                        continue
        except Exception as e:
            print(f"  Error reading file {data_file_path}: {e}. Skipping.")
            continue
        
        if not ip_flow_sequences_from_file:
            print(f"  No valid IP sequences found in {data_file_path}. Skipping.")
            continue

        for target_ip_str, current_text in ip_flow_sequences_from_file.items():
            if target_ip_str not in predefined_patterns:
                # print(f"  IP {target_ip_str} has no predefined pattern. Skipping.")
                continue # Skip IPs for which we don't have a specific pattern
            
            current_pattern = predefined_patterns[target_ip_str]
            print(f"  --- Testing IP: {target_ip_str} with pattern '{current_pattern}' (Text length: {len(current_text)}) ---")
            
            if not current_text:
                print(f"    Text for IP {target_ip_str} is empty. Skipping.")
                continue
            if not current_pattern:
                print(f"    Pattern for IP {target_ip_str} is empty. Skipping.")
                continue

            text_length_chars = len(current_text)
            pattern_length_chars = len(current_pattern)

            # --- Naive matching (streaming) ---
            # IMPORTANT: For performance, ensure print statements inside stream_data and matching functions in functions.py are minimized or disabled.
            stream_for_naive = stream_data(current_text) 
            start_naive = time.perf_counter()
            try:
                naive_matches, naive_comps = naive_stream_matching_with_counts(stream_for_naive, current_pattern)
            except Exception as e:
                print(f"      Error during Naive matching for IP {target_ip_str}: {e}")
                naive_matches, naive_comps = [], -1 # Indicate error
            naive_time = time.perf_counter() - start_naive

            # --- KMP matching (streaming) ---
            stream_for_kmp = stream_data(current_text) # Fresh stream for KMP
            start_kmp = time.perf_counter()
            try:
                kmp_matches, kmp_comps = kmp_stream_matching_with_counts(stream_for_kmp, current_pattern)
            except Exception as e:
                print(f"      Error during KMP matching for IP {target_ip_str}: {e}")
                kmp_matches, kmp_comps = [], -1 # Indicate error
            kmp_time = time.perf_counter() - start_kmp

            # Compute ratios
            speedup_time = (naive_time / kmp_time) if kmp_time > 0 else float('inf')
            reduction_comps = (naive_comps / kmp_comps) if kmp_comps > 0 and naive_comps >=0 and kmp_comps >=0 else float('inf')
            if naive_comps == 0 and kmp_comps == 0:
                reduction_comps = 1.0 
            if naive_comps < 0 or kmp_comps < 0: # Error case
                speedup_time = float('nan')
                reduction_comps = float('nan')

            all_results.append([
                size_mb, target_ip_str, current_pattern,
                text_length_chars, pattern_length_chars,
                len(naive_matches), naive_time, naive_comps,
                len(kmp_matches), kmp_time, kmp_comps,
                speedup_time, reduction_comps
            ])
            print(f"      Naive: {len(naive_matches):3d} matches, {naive_comps:10d} comps, {naive_time:8.4f}s")
            print(f"      KMP:   {len(kmp_matches):3d} matches, {kmp_comps:10d} comps, {kmp_time:8.4f}s")

    # Save all results to a new CSV file
    output_csv_filename = "main2_custom_pattern_results.csv"
    try:
        with open(output_csv_filename, "w", newline="", encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(all_results)
        print(f"\n✅ All tests complete. Results saved to {output_csv_filename}")
    except IOError as e:
        print(f"Error writing results to CSV {output_csv_filename}: {e}")

if __name__ == "__main__":
    if not os.path.exists("functions.py"):
        print("Error: functions.py not found in the current directory.")
        print("Please ensure it is present to run the tests.")
    else:
        # Example check for one of the augmented files - this is optional
        # and mainly for user feedback if they run the script before generating data.
        example_augmented_file = f"{generated_file_prefix}{target_sizes_mb[0]}mb.txt"
        if not os.path.exists(example_augmented_file):
            print(f"Warning: Example augmented file '{example_augmented_file}' not found.")
            print("Please ensure you have run 'generate_augmented_flows.py' first.")
        main()