import random

def minority_oversampling(data, target_size):
    """
    Oversamples the minority classes in the dataset to reach the target size.
    
    Args:
        data (list): List of original sequences.
        target_size (int): Desired number of sequences after oversampling.
        
    Returns:
        list: Oversampled dataset.
    """
    original_size = len(data)
    oversampled_data = data[:]
    
    # Randomly duplicate minority samples to reach the target size
    while len(oversampled_data) < target_size:
        sample = random.choice(data)
        oversampled_data.append(sample)
    
    return oversampled_data

def generate_variable_length_sequences(oversampled_sequences, text_lengths):
    """
    Generates sequences with variable lengths from the oversampled data.
    
    Args:
        oversampled_sequences (list): List of oversampled sequences.
        text_lengths (list): List of desired text lengths.
        
    Returns:
        list: Formatted variable-length sequences.
    """
    generated_sequences = []
    for i, seq in enumerate(oversampled_sequences):
        length = random.choice(text_lengths)  # Choose a random text length from the specified sizes
        # Adjust to the desired length
        new_sequence = (seq * (length // len(seq))) + seq[:length % len(seq)]
        formatted_sequence = f"{i}: {new_sequence}"  # Correctly use the incrementing index
        generated_sequences.append(formatted_sequence)
    return generated_sequences

def main(input_path, output_path, target_size):
    # Load the original sequences from the input file
    with open(input_path, "r") as file:
        original_sequences = [line.strip().split(": ", 1)[1] for line in file.readlines()]

    # Apply minority oversampling to generate 20 to 50 sequences
    oversampled_sequences = minority_oversampling(original_sequences, target_size=random.randint(20, 50))

    # Define the text lengths based on Paper 1 (10k, 50k, 100k)
    text_lengths = [10000, 50000, 100000]

    # Generate new sequences with variable lengths and correct indexing
    generated_sequences = generate_variable_length_sequences(oversampled_sequences, text_lengths)

    # Save the generated data to a new file
    with open(output_path, "w") as file:
        file.write("\n".join(generated_sequences) + "\n")

    print(f"Dataset generated successfully with {len(generated_sequences)} sequences at {output_path}")

# Example usage
input_path = "flow_sequences.txt"
output_path = "oversampled_flow_sequences.txt"
target_size = 50  # Maximum number of sequences
main(input_path, output_path, target_size)