#!/bin/bash
#output_dir=$(realpath "$1")
output_dir="$1"

echo looking in directory "$output_dir" for final_commits.txt

cd "$output_dir"
for x in $(cat final_commits.txt); do
  user=$(echo "$x" | awk -F "," '{print $1}')
	repo=$(echo "$x" | awk -F "," '{print $3}')
	if [[ ! -d $user ]]; then
	  echo "Attempting to clone [$x] with 'git clone $repo $user' ..."
	  git clone $repo $user
	else
	  echo "Skipped $user as directory exists."
	fi
done

for x in $(cat final_commits.txt); do
  cd $output_dir
	user=$(echo "$x" | awk -F "," '{print $1}')
	commit=$(echo "$x" | awk -F "," '{print $2}')
	repo=$(echo "$x" | awk -F "," '{print $3}')

	if [[ -z "$commit" ]]; then
	  echo "ERROR: commit empty for user $user in submission: [$x]"
	else
    echo "Attempting to reset [$x] to given commit '$commit' ..."
    cd $user && git reset --hard $commit

    # Let's check that we now have the right commit
    current_commit=$(git rev-parse --verify HEAD)
    if [[ "$commit" != "$current_commit" ]]; then
      echo "ERROR: commit not set correctly for $user in submission: [$x]"
    fi
  fi
done

echo "Please run"
echo 'bash check.sh "$output_dir" "log.txt"'
echo ""
