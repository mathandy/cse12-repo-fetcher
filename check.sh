#!/bin/bash
output_dir=$(realpath "$1")

if [[ -z "$2" ]]; then
  log_path=$(realpath $2)
else
  log_path=$(realpath log.txt)
fi

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
