#!/bin/bash
# This script sets PYTHONPATH to include the current directory
# and runs the query script

# Activate virtual environment
source venv/bin/activate

# Set Python path to include the current directory
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run the query script with the provided arguments
python scripts/query_knowledge_base.py "$@" 