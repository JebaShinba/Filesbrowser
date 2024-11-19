#!/bin/bash

# Define the location for the HTML report (path will differ based on the OS)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
  # Windows-style path (for Git Bash or Cygwin)
  REPORT_FILE="C:/Users/jebas/Filesbrowser/report.html"
else
  # Unix-style path (Linux/macOS)
  REPORT_FILE="$HOME/Filesbrowser/report.html"
fi

# Ensure the report file's parent directory exists
mkdir -p "$(dirname "$REPORT_FILE")"

# Run pytest for the first test file (invalid login)
pytest login_testcases/test_invalid_login.py --html=$REPORT_FILE --self-contained-html

# Check if the first test run was successful
if [ $? -ne 0 ]; then
  echo "Tests failed for invalid login!"
  exit 1
fi

# Run pytest for the second test file (valid login)
pytest login_testcases/test_valid_login.py --html=$REPORT_FILE --self-contained-html

# Check if the second test run was successful
if [ $? -ne 0 ]; then
  echo "Tests failed for valid login!"
  exit 1
fi

# Final message indicating success
echo "Tests completed successfully. HTML report generated: $REPORT_FILE"

