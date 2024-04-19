#!/bin/bash

# Change to the directory of the script
cd "$(dirname "$0")" || exit

# Install requirements
pip install -r requirements.txt

# Run main script
python3 src/main.py
