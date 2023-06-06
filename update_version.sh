#!/bin/bash

# Read the current version from the VERSION file
current_version=$(cat VERSION)

# Extract major, minor, and patch version numbers
major=$(echo "$current_version" | awk -F'.' '{print $1}' | tr -d 'v')
minor=$(echo "$current_version" | awk -F'.' '{print $2}')
patch=$(echo "$current_version" | awk -F'.' '{print $3}')

# Increment the version
if [[ $patch -lt 9 ]]; then
  ((patch++))
elif [[ $minor -lt 9 ]]; then
  patch=0
  ((minor++))
else
  patch=0
  minor=0
  ((major++))
fi

# Update the version in the VERSION file
new_version="v$major.$minor.$patch"
echo "$new_version" > VERSION

# Display the updated version
echo "Updated version: $new_version"
