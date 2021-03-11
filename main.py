#!/usr/bin/env python
"""CSE 12 GITLAB Repo Downloader"""
import pandas as pd
from dateutil.parser import parse as parse_timestamp
import os


GOOGLE_FORM_RESPONSE_CSV = 'Lab3_W21_responses.csv'
OUTPUT_DIR = 'repos'

# this is the key used to get the right data columns from the csv
GOOGLE_FORM_COLUMN_LABELS = {
    'cruz_id': 'Email Address',
    'commit': 'What is the git commit ID of your final submission?',
    'timestamp': 'Timestamp',
    'email': 'Email Address',
}


# Edit this to change repo URL formatting
def user2repo(cruz_id):
    return f'git@git.ucsc.edu:cse-12/winter21/{cruz_id}.git'


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
            # note there should be no spaces in the below string
            # but students often add spaces where they shouldn't be
            # since bash doesn't play well with unexpected spaces, we'll
            # replace them all with underscores
            f.write(f'{cruz_id},{commit},{repo}\n'.replace(' ', '_'))
            commits_to_download.append((cruz_id, commit, repo))

    log_path = os.path.join(output_dir, 'log.txt')
    download_command = f'bash download_script.sh "{output_dir}" 2>&1 | tee "{log_path}"'
    verify_command = f'bash check.sh "{output_dir}" "{log_path}"'
    print(
        f"Final submission list created.  Now let's download them and "
        f"verify we got what we expected.  If all goes well below and "
        f"you're not on Windows, the following will happen "
        f"automatically and this text will fly by without you "
        f"noticing.  If you are on Windows you'll want to open git "
        f"bash and do the following.\n"
        f"\n"
        f"\tTo download repos, please run\n"
        f'\t\t{download_command}\n'
        f"\t\n"
        f"\tNote that you'll need to look at '{log_path}' for errors.\n"
        f"\tE.g. using\n"
        f'\t\tcat "{log_path}" | grep fatal\n'
        f"\tor\n"
        f'\t\tcat "{log_path}" | grep download_script.sh\n'
        f"\t\n"
        f"\tThen you'll want to run\n"
        f"\t\t{verify_command}\n"
        f"\t\n"
    )

    print(f"Running `{download_command}`...")
    os.system(download_command)

    print(f"Running `{verify_command}`...")
    os.system(verify_command)


if __name__ == '__main__':
    main(
        google_form_response_csv_path=GOOGLE_FORM_RESPONSE_CSV,
        output_dir=OUTPUT_DIR,
        headers=GOOGLE_FORM_COLUMN_LABELS
    )
