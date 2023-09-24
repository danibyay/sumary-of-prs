import requests
import json
from datetime import datetime, timedelta
from dateutil import parser, tz 
import sys

# Use the github API to list all pull requests from a given repository
# Returns a list of dictionaries, each pull request object is a dictionary
def get_pull_requests_data(owner, repo, token):
  api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
  headers = {
    "Accept": "application/vnd.github+json", 
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28" 
  }
  response = requests.get(api_url, headers=headers)
  return response.json()


# Trim down the list of PRs to only have those that have been created in the last week
# Returns a list of dictionaries
def filter_prs_by_age(list_of_prs):
  filtered_list = []
  # get a datetime object of the date of one week ago
  now = datetime.now(tz=tz.tzlocal())
  one_week_ago = now + timedelta(days=-7)
  # evaluate each pr's created_at attribute
  for pr in list_of_prs:
    pr_date_string = pr["created_at"]
    pr_datetime_object = parser.parse(pr_date_string)
    if pr_datetime_object >= one_week_ago:
      filtered_list.append(pr)
  return filtered_list

all_prs = get_pull_requests_data("opentofu", "opentofu", str(sys.argv[1]))
desired_prs = filter_prs_by_age(all_prs)




## Relevant properties
# state, title, html_url
# draft
# created_at, 
# updated_at, closed_at, merged_at no
# body? no


# example
# "created_at": "2011-04-10T20:09:31Z",
