#!/bin/bash

get_abs_filename() {
  # credit: https://stackoverflow.com/questions/3915040
  echo "$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
}

#output_dir=$(realpath "$1")
#log_path=$(realpath "$2")
#output_dir="$1"
#log_path="$2"
output_dir=$(get_abs_filename "$1")
log_path=$(get_abs_filename "$2")

echo looking in directory "$output_dir"
cd "$output_dir"

echo ""
echo "Let's check some numbers."
echo "-------------------------"
echo "Actual number of dirs in output dir: $(ls -d */ | wc -l)"
echo "Expected number of dirs: $(cat final_commits.txt | wc -l)"

echo ""
echo "Let's check in $log_path for errors."
echo ""
echo "First, for errors git threw:"
echo "----------------------------"
cat "$log_path" | grep fatal
echo ""
cat "$log_path" | grep download_script.txt


echo ""
echo "Next, let's check if all the commit numbers were as expected"
echo "------------------------------------------------------------"
cat "$log_path" | grep ERROR
