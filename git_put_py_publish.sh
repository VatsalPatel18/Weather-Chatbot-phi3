#!/bin/bash

# SSH to GitHub
ssh -T git@github.com

# Update version using Poetry
poetry version patch

# Publish to PyPI using Poetry
poetry publish --build

# Add changes to Git
git add -A

# Commit changes
git commit -m "Revised code"

# Push changes to GitHub
git push origin master


