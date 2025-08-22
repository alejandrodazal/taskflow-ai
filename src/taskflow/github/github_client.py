from github import Github
from typing import Dict, Any, Optional, List
from taskflow.config import settings

class GitHubClient:
    def __init__(self):
        self.client = Github(settings.github_token)
        self.repo = self.client.get_repo(settings.github_repo)
    
    def create_issue(self, title: str, body: str, labels: List[str] = None) -> Dict[str, Any]:
        issue = self.repo.create_issue(title=title, body=body, labels=labels)
        return {
            'number': issue.number,
            'title': issue.title,
            'body': issue.body,
            'state': issue.state,
            'url': issue.html_url
        }
    
    def update_issue(self, issue_number: int, **kwargs) -> Dict[str, Any]:
        issue = self.repo.get_issue(issue_number)
        issue.edit(**kwargs)
        return {
            'number': issue.number,
            'title': issue.title,
            'body': issue.body,
            'state': issue.state,
            'url': issue.html_url
        }
    
    def close_issue(self, issue_number: int, comment: str = None) -> Dict[str, Any]:
        issue = self.repo.get_issue(issue_number)
        if comment:
            issue.create_comment(comment)
        issue.edit(state='closed')
        return {
            'number': issue.number,
            'title': issue.title,
            'body': issue.body,
            'state': issue.state,
            'url': issue.html_url
        }

    def get_repo_info(self) -> Dict[str, Any]:
        return {
            'full_name': self.repo.full_name,
            'description': self.repo.description,
            'url': self.repo.html_url
        }