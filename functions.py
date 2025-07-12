## Pattern matching functions (Streaming Focus)
# This file contains functions for pattern matching in character streams.

import time
from collections import deque

def stream_data(data, chunk_size=1):
    """
    Simulate streaming data character by character.
    """
    # print(f"Starting stream of text: '{data}'")
    for i in range(0, len(data), chunk_size):
        current_chunk = data[i : i + chunk_size]
        for char_in_chunk in current_chunk:
            # print(f"  Stream yielding: '{char_in_chunk}'")
            yield char_in_chunk
    print("  Stream ended")

# --- LPS Computation (Helper for KMP) ---
def compute_lps(pattern): # Without counts
    m = len(pattern)
    if m == 0: return []
    lps = [0] * m
    j = 0 # length of the previous longest prefix suffix
    i = 1
    while i < m:
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j
            i += 1
        else:
            if j != 0:
                j = lps[j-1]
            else:
                lps[i] = 0
                i += 1
    return lps

def compute_lps_with_counts(pattern):
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    lps_comparisons = 0
    if m == 0: return [], 0
    while i < m:
        lps_comparisons += 1
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps, lps_comparisons

# --- Naive Algorithm (Streaming) ---
def naive_stream_matching(stream, pattern):
    window = deque(maxlen=len(pattern))
    matches = []
    position = 0
    if not pattern: return []
    print(f"\nNaive streaming started (pattern: '{pattern}')")
    try:
        while True:
            char = next(stream)
            # print(f"  Naive received: '{char}' at position {position}")
            window.append(char)
            if len(window) == len(pattern):
                current_window = ''.join(window)
                # print(f"    Window full: '{current_window}' vs pattern")
                if current_window == pattern:
                    print(f"    Match found at position {position - len(pattern) + 1}")
                    matches.append(position - len(pattern) + 1)
            position += 1
    except StopIteration:
        print("  Naive reached end of stream")
        pass
    return matches

def naive_stream_matching_with_counts(stream, pattern):
    comparisons = 0
    window = deque(maxlen=len(pattern))
    matches = []
    position = 0
    if not pattern: return [], 0
    print(f"\nNaive streaming with counts started (pattern: '{pattern}')")
    try:
        while True:
            char = next(stream)
            # print(f"  Naive received: '{char}' at position {position}")
            window.append(char)
            if len(window) == len(pattern):
                current_window_str = ''.join(window)
                # print(f"    Window full: '{current_window_str}' vs pattern")
                match_this_window = True
                for k in range(len(pattern)):
                    comparisons += 1
                    # print(f"      Comparing '{current_window_str[k]}' with '{pattern[k]}'")
                    if current_window_str[k] != pattern[k]:
                        match_this_window = False
                        # print("      Mismatch found, breaking")
                        break
                if match_this_window:
                    # print(f"    Match found at position {position - len(pattern) + 1}")
                    matches.append(position - len(pattern) + 1)
            position += 1
    except StopIteration:
        print("  Naive reached end of stream")
        pass
    print(f"  Total comparisons made: {comparisons}")
    return matches, comparisons

# --- KMP Algorithm (Streaming - processes stream char by char) ---
def kmp_stream_matching(stream, pattern):
    m = len(pattern)
    if m == 0: return []
    lps = compute_lps(pattern)
    print(f"\nKMP streaming started (pattern: '{pattern}')")
    print(f"  Computed LPS array: {lps}")
    j = 0  # index for pattern[]
    i = 0  # index for current character position in stream
    matches = []
    try:
        while True:
            char = next(stream)
            # print(f"  KMP received: '{char}' at position {i}")
            while j > 0 and char != pattern[j]:
                # print(f"    Mismatch, shifting j from {j} to {lps[j-1]}")
                j = lps[j - 1]
            if char == pattern[j]:
                # print(f"    Matched with pattern[{j}]")
                j += 1
            if j == m:
                print(f"    Complete match found at position {i - m + 1}")
                matches.append(i - m + 1)
                j = lps[j - 1]
            i += 1
    except StopIteration:
        print("  KMP reached end of stream")
        pass
    return matches

def kmp_stream_matching_with_counts(stream, pattern):
    m = len(pattern)
    if m == 0: return [], 0
    lps, lps_comparisons = compute_lps_with_counts(pattern)
    print(f"\nKMP streaming with counts started (pattern: '{pattern}')")
    print(f"  Computed LPS array: {lps}")
    print(f"  LPS computation took {lps_comparisons} comparisons")
    search_comparisons = 0
    j = 0
    i = 0
    matches = []
    try:
        while True:
            char = next(stream)
            # print(f"  KMP received: '{char}' at position {i}")
            while j > 0 and char != pattern[j]:
                search_comparisons += 1
                # print(f"    Comparison {search_comparisons}: '{char}' != '{pattern[j]}' at j={j}")
                # print(f"    Shifting j from {j} to {lps[j-1]}")
                j = lps[j - 1]
            
            search_comparisons += 1
            # print(f"    Comparison {search_comparisons}: '{char}' vs '{pattern[j]}' at j={j}")
            if char == pattern[j]:
                # print(f"      Match! Advancing j to {j+1}")
                j += 1
            
            if j == m:
                # print(f"    Complete match found at position {i - m + 1}")
                matches.append(i - m + 1)
                j = lps[j - 1]
            
            i += 1
    except StopIteration:
        print("  KMP reached end of stream")
        pass
        
    total_comparisons = lps_comparisons + search_comparisons
    print(f"  Total comparisons: {total_comparisons} (LPS: {lps_comparisons}, Search: {search_comparisons})")
    return matches, total_comparisons
