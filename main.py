# CSE 12 GITLAB Repo Downloader
import pandas as pd
from dateutil.parser import parse as parse_timestamp
import os


GOOGLE_FORM_RESPONSE_CSV = 'Lab4_f20_responses.csv'
OUTPUT_DIR = '/Users/Andy/Downloads/lab4-repos'

GOOGLE_FORM_COLUMN_LABELS = {
    'cruz_id': 'What is your CruzID',
    'commit': 'What is the git commit ID of your final submission?',
    'timestamp': 'Timestamp',
    'email': 'Email Address',
}


# Edit this to change repo URL formatting
def user2repo(cruz_id):
    return f'git@git.ucsc.edu:cse012/fall20/{cruz_id}.git'


def main(google_form_response_csv_path, output_dir, headers):
    submissions = pd.read_csv(google_form_response_csv_path)
    # print(responses.columns)  # <-- to see column labels available

    # instead of relying on pandas to sort by date,
    # let's use datetime (and parse the date with dateutil)
    def get_most_recent_submission(submissions):
        return max(
            submissions.iterrows(),
            # enumerates entries, ir=(index, row)
            key=lambda ir: parse_timestamp(ir[1][headers['timestamp']])
        )[1]

    # simplify data structure to an array
    simplified_submissions = []
    for _, submission in submissions.iterrows():
        cruz_id = submission[headers['cruz_id']].strip()
        commit = submission[headers['commit']].strip()
        email = submission[headers['email']].strip()
        timestamp = parse_timestamp(submission[headers['timestamp']].strip())

        # some students write cruz_id funny or give sid #,
        # so use email if possible
        if email.endswith('@ucsc.edu'):
            cruz_id = email[:email.index('@')]

        simplified_submissions.append((timestamp, cruz_id, commit))

    # sort by timestamp
    simplified_submissions.sort()

    # since they're sorted (and assuming all ids fixed),
    # this will get the final commit for each id
    final_submissions = dict()
    for timestamp, cruz_id, commit in simplified_submissions:
        final_submissions[cruz_id] = commit

    # make output dir to store repos and list of final commits
    os.makedirs(output_dir, exist_ok=True)

    # write list of cruz_id,commit pairs to txt file
    commits_to_download = []
    output_commit_list_path = os.path.join(output_dir, 'final_commits.txt')
    with open(output_commit_list_path, 'w') as f:
        for cruz_id, commit in final_submissions.items():
            repo = user2repo(cruz_id)
            f.write(f'{cruz_id},{commit},{repo}\n')
            commits_to_download.append((cruz_id, commit, repo))

    print(
        f"Final submission list created.  To download repos, please run\n"
        f"\tbash download_script.sh {output_dir} 2>&1 | tee log.txt\n"
        f"\n"
        f"Note that you'll need to look at log.txt for errors.\n"
        f"E.g. using\n"
        f"\tcat log.txt | grep fatal\n"
        f"or\n"
        f"\tcat log.txt | grep download_script.sh\n"
        f"\n"
        f"Then you'll want to run\n"
        f"\tbash check_dirs\n"
        f"\n"
        f"If all goes well below (e.g. you're not using windows or fish) this "
        f"will be done for you."
    )

    download_command = f"bash download_script.sh {output_dir} 2>&1 | tee {output_dir}/log.txt"
    print(f"Running `{download_command}`...")
    os.system(download_command)

    checker_command = f"bash check.sh {output_dir} {output_dir}/log.txt"
    print(f"Running `{checker_command}`...")
    os.system(checker_command)


if __name__ == '__main__':
    main(
        google_form_response_csv_path=GOOGLE_FORM_RESPONSE_CSV,
        output_dir=OUTPUT_DIR,
        headers=GOOGLE_FORM_COLUMN_LABELS
    )
