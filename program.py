import requests
import json
from datetime import datetime, timedelta
from dateutil import parser, tz 
import sys


def get_pull_requests_data(owner, repo, token):
  api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
  headers = {
    "Accept": "application/vnd.github+json", 
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28" 
  }
  response = requests.get(api_url, headers=headers)
  return response.json()


response_j = get_pull_requests_data("opentofu", "opentofu", str(sys.argv[1]))

date_1 = response_j[1]["created_at"]

print(f"raw date is {date_1}")

date_object = parser.parse(date_1)
print(f"parsed date is {date_object}")
now = datetime.now(tz=tz.tzlocal())
one_week_ago = now + timedelta(days=-7)
print(f"one week ago was {one_week_ago}")

if date_object >= one_week_ago:
  print("the first PR is less than a week old")
else:
  print("the first PR is more then a week old") 

## Relevant properties
# state, title, html_url
# draft
# created_at, 
# updated_at, closed_at, merged_at no
# body? no


# example
# "created_at": "2011-04-10T20:09:31Z",
