import sys

import requests

CODEFORCES_API_STATUS = 'https://codeforces.com/api/user.status'

for line in sys.stdin.readlines():
    handle = line.strip()
    res = requests.get(CODEFORCES_API_STATUS, params={
        "handle": handle
    })
    submissions = res.json()['result']
    problems = [submission['problem'] for submission in submissions]
    problems = set((problem['contestId'], problem['index'])
                   for problem in problems)
    print(handle, len(problems))
