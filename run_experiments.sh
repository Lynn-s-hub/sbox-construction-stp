#!/bin/bash

N=$1  # Get number of runs from command line

if [ -z "$N" ]; then
    echo "Usage: $0 <number_of_runs>"
    exit 1
fi

echo "Starting $N automatic experiments..."
echo "=========================================="

# Record experiment start time
experiment_start_time=$(date +%s.%N)
experiment_start_readable=$(date '+%Y-%m-%d %H:%M:%S')

for ((i=1; i<=N; i++))
do
    echo "Run $i starting..."
    run_start_time=$(date +%s.%N)
    
    # Run your four commands
    stp test.cvc > test.result
    python getsolution.py
    
    run_end_time=$(date +%s.%N)
    
    # Calculate run time and cumulative time
    run_duration=$(echo "$run_end_time - $run_start_time" | bc)
    cumulative_time=$(echo "$run_end_time - $experiment_start_time" | bc)
    
    echo "Run $i completed"
    echo "Run time: ${run_duration} seconds"
    echo "Cumulative time: ${cumulative_time} seconds"
    echo "------------------------------------------"
    
    # Optional: Pause between runs
    sleep 1
done

total_duration=$(echo "$(date +%s.%N) - $experiment_start_time" | bc)
echo "All $N experiments completed!"
echo "Start time: $experiment_start_readable"
echo "Total time: ${total_duration} seconds"
