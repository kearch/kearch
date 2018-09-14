# Benchmark tool for Kearch
This is a benchmark tool for Kearch.  
# How to use
- Install siege
- Change the limit of the number of concurrent connection in `~/.siege/siege.conf`  
  I recommend you to change `limit = 10000`
- `cd kearch/benchmark && python3 benchmarker.py`
# Notice
Sometime, siege cannot access the search engine and `Transaction` become to 0.  
I cannot find the reason.
