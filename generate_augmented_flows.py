import random
import os
import tracemalloc

def augment_sequence(original_sequence, target_length_chars):
    """
    Augments a sequence to a target length by repeating and shuffling.
    """
    if not original_sequence:
        # If the original sequence is empty, return a sequence of 'a's
        # or handle as an error. For now, fill with 'a'.
        print("Warning: Original sequence is empty. Filling with 'a'.")
        return 'a' * target_length_chars
    if target_length_chars <= 0:
        return ""

    augmented_seq = []
    original_list = list(original_sequence)
    
    while len(augmented_seq) < target_length_chars:
        # Append a shuffled version of the original sequence
        # or parts of it to introduce some variability.
        # For very long target lengths, repeating the original is inevitable.
        chunk = original_list[:] # Make a copy
        random.shuffle(chunk)
        augmented_seq.extend(chunk)
        
    return "".join(augmented_seq[:target_length_chars])

def generate_large_flow_file(original_file_path, target_mb_size, output_file_path):
    """
    Generates a large flow sequence file by augmenting sequences from the original file.
    """
    try:
        with open(original_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Original file '{original_file_path}' not found.")
        return

    if not lines:
        print(f"Error: Original file '{original_file_path}' is empty.")
        return

    ip_original_sequences = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            ip_str, seq_str = line.split(':', 1)
            ip_original_sequences[ip_str.strip()] = seq_str.strip()
        except ValueError:
            print(f"Warning: Skipping malformed line in '{original_file_path}': {line}")
            continue
    
    if not ip_original_sequences:
        print("Error: No valid IP sequences found in the original file.")
        return

    num_ips = len(ip_original_sequences)
    target_total_bytes = target_mb_size * 1024 * 1024

    # Estimate overhead per line (e.g., "0: " + newline char)
    # This is an approximation.
    # Average IP string length (e.g., "1", "10") + ": " (2 chars) + "\n" (1 char)
    avg_ip_str_len = sum(len(ip) for ip in ip_original_sequences.keys()) / num_ips
    avg_overhead_per_line = avg_ip_str_len + 2 + 1 
    total_overhead_bytes = num_ips * avg_overhead_per_line

    if target_total_bytes <= total_overhead_bytes:
        print(f"Error: Target size {target_mb_size}MB is too small to accommodate IP prefixes for {num_ips} IPs.")
        return
        
    target_sequence_bytes_total = target_total_bytes - total_overhead_bytes
    chars_per_ip_sequence = int(target_sequence_bytes_total / num_ips)

    if chars_per_ip_sequence <= 0:
        print(f"Error: Calculated characters per IP sequence is non-positive ({chars_per_ip_sequence}). Target size might be too small relative to the number of IPs and overhead.")
        return

    print(f"Generating '{output_file_path}' ({target_mb_size}MB)...")
    print(f"  Target characters per IP sequence: {chars_per_ip_sequence}")

    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        for ip_str, original_seq in ip_original_sequences.items():
            augmented_seq = augment_sequence(original_seq, chars_per_ip_sequence)
            outfile.write(f"{ip_str}: {augmented_seq}\n")
    
    print(f"Successfully generated '{output_file_path}' (Actual size: {os.path.getsize(output_file_path) / (1024*1024):.2f}MB)")

def generate_synthetic_sequence(sequences, min_length=10000, max_length=100000):
    length = random.randint(min_length, max_length)
    synthetic_sequence = ''
    while len(synthetic_sequence) < length:
        seq = random.choice(sequences)
        part = seq[:min(length - len(synthetic_sequence), len(seq))]
        synthetic_sequence += part
    return synthetic_sequence

def generate_synthetic_dataset(input_file, output_file, num_sequences=1000, max_file_size=10 * 1024 * 1024):
    sequences = []
    with open(input_file, 'r') as file:
        for line in file:
            # If colon, treat as IP: sequence, else just sequence
            if ':' in line:
                _, seq = line.strip().split(':', 1)
                sequences.append(seq.strip())
            else:
                sequences.append(line.strip())
    with open(output_file, 'w') as file:
        for _ in range(num_sequences):
            synthetic_sequence = generate_synthetic_sequence(sequences)
            if file.tell() + len(synthetic_sequence) > max_file_size:
                break
            file.write(synthetic_sequence + '\n')
    print(f"Generated synthetic dataset saved to {output_file}")

if __name__ == "__main__":
    original_file = "flow_sequences.txt" # Make sure this file exists in the same directory or provide full path
    target_sizes_mb = [10, 20, 30, 40, 50] # Define the target file sizes in MB

    if not os.path.exists(original_file):
        print(f"Error: The input file '{original_file}' does not exist in the current directory: {os.getcwd()}")
        print("Please create it or provide the correct path.")
    else:
        for size_mb in target_sizes_mb:
            output_filename = f"flow_sequences_{size_mb}mb.txt"
            generate_large_flow_file(original_file, size_mb, output_filename)
        print("\nAll files generated.")

    # --- Synthetic sequence generation with memory measurement ---
    tracemalloc.start()
    generate_synthetic_dataset(original_file, 'synthetic_sequences.txt')
    current, peak = tracemalloc.get_traced_memory()
    print(f"Peak memory usage for synthetic generation: {peak / (1024 * 1024):.2f} MB")
    tracemalloc.stop() 