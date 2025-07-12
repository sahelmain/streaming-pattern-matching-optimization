## imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import time
from collections import deque

# Load the dataset
file_path = "cs448b_ipasn.csv"
df = pd.read_csv(file_path)

# Define known compromise dates and IPs
compromise_info = {
    1: "2006-08-24",
    5: "2006-09-04",
    4: "2006-09-18",
    3: "2006-09-26",
    6: "2006-09-26"
}

# Show basic info and a sample
df_info = df.info()
df_head = df.head()

df.describe(), df_head

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Group by date and IP to get daily flow volume
daily_flows = df.groupby(['date', 'l_ipn'])['f'].sum().reset_index()

# Pivot for easier visualization
pivot_df = daily_flows.pivot(index='date', columns='l_ipn', values='f')

# Plot the flow spikes for each IP
plt.figure(figsize=(15, 7))
sns.lineplot(data=pivot_df)
plt.title("Daily Flow Volume per Local IP (l_ipn)")
plt.xlabel("Date")
plt.ylabel("Total Flows (f)")
plt.legend(title="Local IP", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.grid(True)
# plt.show()

# Step 1: Ensure data is sorted by IP and date
df_sorted = df.sort_values(by=['l_ipn', 'date'])

# Step 2: Create ASN-to-character mapping (global across all IPs)
unique_asns = df_sorted['r_asn'].unique()
asn_to_char = {asn: chr(65 + i % 26) + (str(i // 26) if i >= 26 else '') for i, asn in enumerate(unique_asns)}

# Step 3: Build per-IP ASN sequences (sequence of remote connections)
ip_asn_sequences = defaultdict(list)
for _, row in df_sorted.iterrows():
    ip = row['l_ipn']
    asn = row['r_asn']
    ip_asn_sequences[ip].append(asn_to_char[asn])
ip_asn_sequences_str = {ip: ''.join(seq) for ip, seq in ip_asn_sequences.items()}

# Step 4: Build per-IP flow-level sequences (summed per day, categorized as a/b/c/d)
# Group by IP and date, summing flows
daily_flows = df.groupby(['l_ipn', 'date'])['f'].sum().reset_index()

# Define buckets: a = low, b = medium, c = high, d = very high
def flow_bucket(f):
    if f < 10:
        return 'a'
    elif f < 100:
        return 'b'
    elif f < 1000:
        return 'c'
    else:
        return 'd'

# Apply bucketing to create flow-level strings
daily_flows['flow_level'] = daily_flows['f'].apply(flow_bucket)

# Build sequence per IP
ip_flow_sequences = defaultdict(str)
for _, row in daily_flows.iterrows():
    ip = row['l_ipn']
    ip_flow_sequences[ip] += row['flow_level']

# Return first 100 characters of both encodings for preview
preview_sequences = {
    ip: {
        "flow_levels": ip_flow_sequences[ip][:100],
        "asn_sequence": ip_asn_sequences_str[ip][:100]
    }
    for ip in ip_flow_sequences
}

preview_sequences

# Define known compromise dates and IPs
compromise_info = {
    1: "2006-08-24",
    5: "2006-09-04",
    4: "2006-09-18",
    3: "2006-09-26",
    6: "2006-09-26"
}

# Extract a 7-day window before each compromise date for both flow-level and ASN sequences
pattern_window_days = 7
pattern_data = {}

for ip, date_str in compromise_info.items():
    compromise_date = pd.to_datetime(date_str)
    start_date = compromise_date - pd.Timedelta(days=pattern_window_days)

    # Flow pattern extraction
    daily_flows = df[df['l_ipn'] == ip].groupby(['date'])['f'].sum().reset_index()
    daily_flows = daily_flows[(daily_flows['date'] >= start_date) & (daily_flows['date'] < compromise_date)]
    daily_flows['flow_level'] = daily_flows['f'].apply(lambda f: 'a' if f < 10 else 'b' if f < 100 else 'c' if f < 1000 else 'd')
    flow_pattern = ''.join(daily_flows.sort_values('date')['flow_level'].tolist())

    # ASN pattern extraction
    asn_df = df[(df['l_ipn'] == ip) & (df['date'] >= start_date) & (df['date'] < compromise_date)].sort_values('date')
    asn_sequence = ''.join([asn_to_char[asn] for asn in asn_df['r_asn']])

    pattern_data[ip] = {
        'date_range': f"{start_date.date()} to {compromise_date.date()}",
        'flow_pattern': flow_pattern,
        'asn_pattern': asn_sequence[:100]  # limit for preview
    }

pattern_data

# compare string
# def str_match(str1, str2):
#     match = True
#     if len(str1) == len(str2):
#         for i in range(len(str1)):
#             if str1[i] != str2[i]:
#                 match = False
#                 break
#     return match

def StreamingMatcher(text, delay=0.05):
    for char in text:
        yield char
        time.sleep(delay)

def str_match(str1, str2):
    if len(str1) != len(str2):
        return False
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            return False
    return True
# Naive pattern matching
def naive_stream_matching(text, pattern, delay=0.05):
    """
    Simulate pattern matching using naive for stream data
    """
    m = len(pattern)

    window = deque(maxlen=m)
    matches = []
    index = -1

    for char in StreamingMatcher(text, delay):
        index = index + 1
        window.append(char)
        if len(window) == m:
            currentWindow = "".join(window)
            if str_match(currentWindow, pattern):
                matches.append(index - m + 1)
    return matches

    # for index, char in enumerate(text):
    #     window.append(char)
    #     current_window = "".join(window)

    #     # if str_match(current_window, pattern):
    #     #     match_index = index - len(pattern) + 1
    #     #     matches.append(match_index)
    #     if current_window == pattern:
    #         match_index = index - len(pattern) + 1
    #         matches.append(match_index)
        
    #     # time.sleep(delay)
    # return matches


# longest prefix-suffix function
def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    j = 0
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

# KMP pattern matching
def kmp_stream_matching(text, pattern, delay=0.05):
    # n = len(text)
    m = len(pattern)
    lps = compute_lps(pattern)
    matches = []
    # i = 0  # index for text
    j = 0  # index for pattern
    index = -1

    for char in StreamingMatcher(text, delay):
        index = index + 1
        while j > 0 and pattern[j] != char:
            j = lps[j-1]
        
        if pattern[j] == char:
            j = j + 1
        
        if j == m:
            matches.append(index - m + 1)
            j = lps[j-1]
    return matches





    # while i < n:
    #     if pattern[j] == text[i]:
    #         i += 1
    #         j += 1
            
    #         if j == m:  # Found a match
    #             matches.append(i - m)  # Record the starting position
    #             j = lps[j-1]  # Look for overlapping matches
    #     else:
    #         if j != 0:  # Mismatch after at least one match
    #             j = lps[j-1]  # Fall back in the pattern
    #         else:  # Mismatch at start
    #             i += 1
                
    #     # time.sleep(delay)  # Simulate stream processing
        
    # return matches
            

    
naive_result = ()



text = ip_flow_sequences[5]
pattern = pattern_data[5]['flow_pattern']

char_delay = 0.05
text_stream = StreamingMatcher(text, char_delay)

start = time.time()
naive_matches = naive_stream_matching(text, pattern, delay=char_delay)
end = time.time()
naive_result = (len(naive_matches), end - start)

print("Results")
print("Naive: matches: " + str(naive_result[0]) + ", runtime: " + str(naive_result[1]))

kmp_result = ()
start = time.time()
kmp_matches = kmp_stream_matching(text, pattern)
end = time.time()
kmp_result = (len(kmp_matches), end - start)

print("Results")
print("KMP: matches: " + str(kmp_result[0]) + ", runtime: " + str(kmp_result[1]))