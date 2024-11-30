#!/bin/bash

count=100

for i in $(seq 1 $count); do
    echo "Running iteration $i..."
    # python3 snake.py -session 100000 -load models/q_table.pkl | grep "Q ="
    python3 snake.py -session 1000000 -load models/q_table.pkl | grep "max length :"
done