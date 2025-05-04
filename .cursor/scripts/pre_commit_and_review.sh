#!/bin/bash

# Script to run pre-commit checks and commit if successful

echo "Running pre-commit checks..."
pre-commit run --all-files

# Check if pre-commit was successful
if [ $? -eq 0 ]; then
    echo "Pre-commit checks passed successfully!"
    
    # Check if there are any staged changes
    if git diff --staged --quiet; then
        echo "No changes are staged for commit."
    else
        # Attempt to commit with the provided message or default message
        commit_message=${1:-"Automated commit after successful pre-commit checks"}
        git commit -m "$commit_message"
        echo "Changes committed successfully with message: $commit_message"
    fi
else
    echo "Pre-commit checks failed. Please fix the issues before committing."
    exit 1
fi 