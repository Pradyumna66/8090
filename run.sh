#!/bin/bash
PYTHON_PATH=$(command -v python)
# "$PYTHON_PATH" calculate_reimbursement.py "$1" "$2" "$3"

/c/Python312/python.exe calculate_reimbursement.py "$1" "$2" "$3" | tr -d '\r'
# python3 calculate_reimbursement.py "$1" "$2" "$3"
# python3 calculate_reimbursement.py "$1" "$2" "$3" | tr -d '\r'