import pandas as pd
from collections import defaultdict
import time
import csv
# from memory_profiler import memory_usage # Keep if you're still using it, otherwise remove

# Correctly import the STREAMING KMP versions from functions.py
from functions import (
    stream_data,
    naive_stream_matching_with_counts,  # Or naive_stream_matching if not counting
    kmp_stream_matching_with_counts     # Or kmp_stream_matching if not counting
)

def main():
    # Debug test with a very small example first
    print("\n=== STREAMING ALGORITHM VERIFICATION TEST ===")
    test_text = "hxxxxxxm"      # A small sample from your flow data
    test_pattern = "xxx"        # A pattern we expect to find
    
    print(f"\nTest Case:")
    print(f"Text: '{test_text}' (length: {len(test_text)})")
    print(f"Pattern: '{test_pattern}' (length: {len(test_pattern)})")
    
    # Test Naive Streaming
    print("\n--- Testing Naive Streaming Algorithm ---")
    stream_for_naive = stream_data(test_text)
    naive_matches, naive_comps = naive_stream_matching_with_counts(stream_for_naive, test_pattern)
    print(f"Naive found {len(naive_matches)} matches at positions: {naive_matches}")
    print(f"Naive made {naive_comps} character comparisons")
    
    # Test KMP Streaming
    print("\n--- Testing KMP Streaming Algorithm ---")
    stream_for_kmp = stream_data(test_text)
    kmp_matches, kmp_comps = kmp_stream_matching_with_counts(stream_for_kmp, test_pattern)
    print(f"KMP found {len(kmp_matches)} matches at positions: {kmp_matches}")
    print(f"KMP made {kmp_comps} character comparisons")
    
    print("\n=== END VERIFICATION TEST ===")
    print("\nProceeding with full dataset analysis...")

    file_path = "cs448b_ipasn.csv"
    df = pd.read_csv(file_path)

    compromise_info = {
        1: "2006-08-24",
        5: "2006-09-04",
        4: "2006-09-18",
        3: "2006-09-26",
        6: "2006-09-26"
    }

    df['date'] = pd.to_datetime(df['date'])
    df_sorted = df.sort_values(by=['l_ipn', 'date'])

    daily_flows = df.groupby(['l_ipn', 'date'])['f'].sum().reset_index()

    x

    daily_flows['flow_level'] = daily_flows['f'].apply(flow_bucket)

    ip_flow_sequences = defaultdict(str)
    for _, row in daily_flows.iterrows():
        ip = row['l_ipn']
        ip_flow_sequences[ip] += row['flow_level']

    flow_patterns_data = {}
    window_days = 7
    for ip, date_str in compromise_info.items():
        compromise_date = pd.to_datetime(date_str)
        start_date = compromise_date - pd.Timedelta(days=window_days)

        flow_segment = df[df['l_ipn'] == ip].groupby(['date'])['f'].sum().reset_index()
        flow_segment = flow_segment[(flow_segment['date'] >= start_date) & (flow_segment['date'] < compromise_date)]
        flow_segment['flow_level'] = flow_segment['f'].apply(flow_bucket)
        flow_pattern_str = ''.join(flow_segment.sort_values('date')['flow_level'].tolist())
        if flow_pattern_str:
            flow_patterns_data[ip] = flow_pattern_str

    # --- ASN Sequence Generation ---
    unique_asns = df_sorted['r_asn'].unique()
    # Create a consistent mapping for ASN characters
    sorted_unique_asns = sorted(list(unique_asns))
    asn_to_char = {asn: chr(65 + i % 26) + (str(i // 26) if i // 26 > 0 else '') for i, asn in enumerate(sorted_unique_asns)}

    ip_asn_sequences_str = defaultdict(str)
    for _, row in df_sorted.iterrows():
        ip_asn_sequences_str[row['l_ipn']] += asn_to_char[row['r_asn']]

    asn_patterns_data = {}
    for ip, date_str in compromise_info.items():
        compromise_date = pd.to_datetime(date_str)
        start_date = compromise_date - pd.Timedelta(days=window_days)
        asn_df_segment = df_sorted[
            (df_sorted['l_ipn'] == ip) &
            (df_sorted['date'] >= start_date) &
            (df_sorted['date'] < compromise_date)
        ]
        # Ensure r_asn exists in asn_to_char, skip if not (should not happen with above generation)
        asn_pattern_str = ''.join([asn_to_char[asn] for asn in asn_df_segment['r_asn'] if asn in asn_to_char])
        if asn_pattern_str:
            asn_patterns_data[ip] = asn_pattern_str
            
    # --- CSV Output Preparation ---
    # Added peak_memory_mb columns back, assuming memory_profiler might be used later or data is fine as 0
    header = [
        "pattern_ip", "target_ip", "data_type",
        "text_length", "pattern_length",
        "naive_match_count", "naive_time_sec", "naive_comparisons", "naive_peak_memory_mb",
        "kmp_match_count", "kmp_time_sec", "kmp_comparisons", "kmp_peak_memory_mb",
        "kmp_speedup_ratio_time", "kmp_reduction_ratio_comps"
    ]

    # --- Function to run tests and collect results ---
    def run_matching_tests(patterns_dict, sequences_dict, data_type_label):
        output_rows_list = []
        print(f"\nRunning tests for {data_type_label} data...")
        for pattern_ip, current_pattern in patterns_dict.items():
            if not current_pattern: 
                print(f"  Skipping Pattern IP {pattern_ip} for {data_type_label} (empty pattern)")
                continue
            # Conditional print for less noise, focus on IP 1 for detailed pattern info
            # if pattern_ip == 1 and data_type_label == "Flow": 
            #    print(f"  Pattern IP: {pattern_ip} (Pattern Length: {len(current_pattern)}, Pattern: '{current_pattern}')")
            # else:
            #    print(f"  Pattern IP: {pattern_ip} (Pattern Length: {len(current_pattern)})")

            for target_ip, current_text in sequences_dict.items():
                if not current_text: 
                    print(f"    Skipping Target IP {target_ip} for {data_type_label} (empty text) with Pattern IP {pattern_ip}")
                    continue
                
                # ***** START DEBUGGING BLOCK for specific case: pattern_ip=1, target_ip=1, type=Flow *****
                if pattern_ip == 1 and target_ip == 1 and data_type_label == "Flow":
                    print(f"\n--- DEBUGGING: Pattern IP {pattern_ip}, Target IP {target_ip}, Type: {data_type_label} ---")
                    print(f"PATTERN from flow_patterns_data[1]: '{current_pattern}' (Length: {len(current_pattern)})")
                    print(f"TEXT from ip_flow_sequences[1]:    '{current_text}' (Length: {len(current_text)}) ")
                    # print(f"PATTERN (first 20): '{current_pattern[:20]}'") # Uncomment if needed
                    # print(f"TEXT (first 100): '{current_text[:100]}'")   # Uncomment if needed
                elif target_ip == 1 and data_type_label == "Flow": # Reduce noise for other patterns against target_ip 1
                     print(f"  Processing Pattern IP: {pattern_ip} vs Target IP: {target_ip} (Text Length: {len(current_text)}, Pattern Length: {len(current_pattern)})")
                # ***** END DEBUGGING BLOCK *****
                
                text_length = len(current_text)
                pattern_length = len(current_pattern)

                # --- Naive matching (streaming) ---
                stream_for_naive = stream_data(current_text) # Create stream
                start_naive = time.perf_counter()
                naive_matches, naive_comps = naive_stream_matching_with_counts(stream_for_naive, current_pattern)
                naive_time = time.perf_counter() - start_naive
                naive_mem_usage = 0 # Placeholder, memory_profiler calls removed for speed

                # --- KMP matching (streaming) ---
                stream_for_kmp = stream_data(current_text) # Create a fresh stream for KMP
                start_kmp = time.perf_counter()
                kmp_matches, kmp_comps = kmp_stream_matching_with_counts(stream_for_kmp, current_pattern)
                kmp_time = time.perf_counter() - start_kmp
                kmp_mem_usage = 0 # Placeholder

                # ***** START DEBUGGING MATCH COUNT for specific case *****
                if pattern_ip == 1 and target_ip == 1 and data_type_label == "Flow":
                    print(f"NAIVE found {len(naive_matches)} matches. Comparisons: {naive_comps}. Time: {naive_time:.6f}s")
                    # print(f"NAIVE matches at indices: {naive_matches}") # Uncomment to see positions
                    print(f"KMP found {len(kmp_matches)} matches. Comparisons: {kmp_comps}. Time: {kmp_time:.6f}s")
                    # print(f"KMP matches at indices: {kmp_matches}") # Uncomment to see positions
                    print(f"--- END DEBUGGING FOR Pattern IP 1 vs Target IP 1 (Flow) ---")
                # ***** END DEBUGGING MATCH COUNT *****

                # Compute ratios
                speedup_time = naive_time / kmp_time if kmp_time > 0 else float('inf')
                reduction_comps = naive_comps / kmp_comps if kmp_comps > 0 else float('inf')
                if naive_comps == 0 and kmp_comps == 0: 
                    reduction_comps = 1.0 

                output_rows_list.append([
                    pattern_ip, target_ip, data_type_label,
                    text_length, pattern_length,
                    len(naive_matches), naive_time, naive_comps, naive_mem_usage,
                    len(kmp_matches), kmp_time, kmp_comps, kmp_mem_usage,
                    speedup_time, reduction_comps
                ])
        return output_rows_list

    # --- Run tests for Flow data ---
    flow_output_rows = run_matching_tests(flow_patterns_data, ip_flow_sequences, "Flow")
    flow_csv_filename = "flow_pattern_matching_streaming_results.csv"
    with open(flow_csv_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(flow_output_rows)
    print(f"✅ Flow pattern matching (streaming) results saved to {flow_csv_filename}")

    # --- Run tests for ASN data ---
    asn_output_rows = run_matching_tests(asn_patterns_data, ip_asn_sequences_str, "ASN")
    asn_csv_filename = "asn_pattern_matching_streaming_results.csv"
    with open(asn_csv_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(asn_output_rows)
    print(f"✅ ASN pattern matching (streaming) results saved to {asn_csv_filename}")

if __name__ == "__main__":
    main()