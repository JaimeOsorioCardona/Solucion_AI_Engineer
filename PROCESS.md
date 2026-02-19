# Process Log - AI Prompts

Here are the 3 key prompts that simulate how I (as an AI Agent) tackled the problem:

## Prompt 1: Optimization Strategy
> "Start by analyzing the provided `messy_router.py`. It contains a nested loop O(N*M) which is inefficient for spatial validation. Refactor this code into a new file `clean_router.py`. Use Python `dataclasses` for better structure and implementing a Spatial Hashing (Grid-based) optimization or a KDTree to reduce the complexity to roughly O(N + M) or O(N log M). Ensure the code includes type hints and follows PEP-8."

## Prompt 2: Log Analysis
> "I have a CSV file `Server_logs.csv` with columns: timestamp, endpoint, response_time_ms, status_code, db_queries. Write a script `analyze_logs.py` using the standard `csv` library (no external dependencies if possible) to calculate the average response time and average DB queries per endpoint. Also, calculate the correlation coefficient between `response_time_ms` and `db_queries` specifically for the `/api/routes` endpoint to confirm if database load is the bottleneck."

## Prompt 3: Caching Architecture
> "Based on the finding that `/api/routes` has high latency due to excessive DB queries, propose a caching solution. Write a file `cache_solution.py` that implements a Python decorator pattern to simulate a Redis cache. The decorator should check a mock Redis client for a key; if it's a hit, return the cached JSON; if it's a miss, execute the function and store the result. ensure it simulates strict checking."
