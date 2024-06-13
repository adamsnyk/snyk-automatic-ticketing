import requests

# Replace with your Snyk API token, organization ID, and other necessary details
SNYK_API_TOKEN = 'YOUR_SNYK_API_TOKEN'
ORG_ID = 'YOUR_ORG_ID'
JIRA_PROJECT_KEY = 'YOUR_JIRA_PROJECT_KEY'
JIRA_ISSUE_TYPE = 'Bug'  # Replace with the appropriate Jira issue type

# Snyk API base URL
BASE_URL = 'https://snyk.io/api/v1'

# Headers for API requests
headers = {
    'Authorization': f'token {SNYK_API_TOKEN}',
    'Content-Type': 'application/json'
}

def get_projects(org_id):
    url = f'{BASE_URL}/org/{org_id}/projects'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['projects']

def get_issues(org_id, project_id):
    url = f'{BASE_URL}/org/{org_id}/project/{project_id}/issues'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['issues']

def create_jira_issue(org_id, project_id, issue):
    url = f'{BASE_URL}/org/{org_id}/project/{project_id}/jira-issue'
    data = {
        'issue': {
            'title': issue['issueData']['title'],
            'severity': issue['issueData']['severity'],
            'url': issue['issueData']['url']
        },
        'jira': {
            'project': {
                'key': JIRA_PROJECT_KEY
            },
            'issueType': {
                'name': JIRA_ISSUE_TYPE
            }
        }
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def main(issue_limit):
    projects = get_projects(ORG_ID)
    
    for project in projects:
        if project['attributes'].get('criticality') == 'high':
            project_id = project['id']
            issues = get_issues(ORG_ID, project_id)
            
            count = 0
            for issue in issues:
                if count >= issue_limit:
                    break
                if issue['issueData']['severity'] in ['high', 'critical']:
                    exploit_maturity = issue['issueData'].get('exploit', {}).get('maturity', '')
                    if exploit_maturity in ['mature', 'proof-of-concept']:
                        # Check if a Jira ticket has already been opened
                        if 'jira' in issue and issue['jira']:
                            continue
                        create_jira_issue(ORG_ID, project_id, issue)
                        count += 1

if __name__ == '__main__':
    issue_limit = int(input("Enter the limit of issues per project to be opened: "))
    main(issue_limit)
