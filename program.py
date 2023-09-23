import requests
import json
token = ""
## This should be at least an env var

## TODO: use github actions to trigger the program and 
## use my token as an env var in github actions

## TODO: can the target email be parametrized in github actions ?

api_url = "https://api.github.com/repos/opentofu/opentofu/pulls"
headers = {
  "Accept": "application/vnd.github+json", 
  "Authorization": f"Bearer {token}",
  "X-GitHub-Api-Version": "2022-11-28" 
}
response = requests.get(api_url, headers=headers)

response_j = response.json()

print(len(response_j))
print()
print(response_j[1])

## Relevant properties
# state, title, html_url
# draft
# created_at, 
# updated_at, closed_at, merged_at no
# body? no