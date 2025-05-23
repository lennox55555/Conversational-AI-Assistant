#!/bin/bash
# run tests with coverage report

# install required packages if needed
pip install -r requirements.txt

# run tests with coverage
python -m pytest test_index.py -v --cov=index --cov-report=term-missing --cov-report=html

# print coverage report
echo "coverage report is available in htmlcov/index.html"

# check if coverage threshold is met
coverage=$(python -m coverage report | grep TOTAL | awk '{print $4}' | tr -d '%')
if (( $(echo "$coverage < 80" | bc -l) )); then
  echo "coverage is $coverage%, which is below the required 80%"
  exit 1
else
  echo "coverage is $coverage%, which meets the required 80%"
fi