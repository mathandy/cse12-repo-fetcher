# CSE 12 GITLAB Repo Downloader

## Requirements
* Unix-like environment.  If you're on windows, 
only the bash scripts used at the end to download and check 
commits won't work.
* python>=3.6  # tested with 3.7.6
* pip install python-dateutil  # tested with 2.8.1
* pandas  # tested with 1.0.3

# Usage
1. Edit the all-caps variables at the top of main.py and 
the gitlab URL in the `user2repo()` function 
2. python main.py # downloads all repos and checkouts correct commit

Note: read the output of main.py -- it will tell you about errors (e.g. incorrect commit hashes).

# Notes on MOSS
If you want to run moss, I'd recommend creating a folder containing one asm file from each student, `cp somecruzid/lab3/lab3.asm moss_dir/somecruzid.asm`
The code snippets in "create-moss-dir.sh" may help with this.  

After creating such a directory, you should be able to submit all files to MOSS using  

`perl moss.pl -l mips *.asm`

# Troubleshooting MOSS
* make sure moss.pl is up to date.
* make sure the `$userid` setting inside moss.pl is correct.
