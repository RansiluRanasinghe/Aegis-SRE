from github import Github
from github.GithubException import GithubException
from app.core.config import settings

class GitHubService:

    def __init__(self):
        self.token = settings.GITHUB_TOKEN
        self.repo_name = settings.GITHUB_REPO

        if self.token:
            self.gh = Github(self.token)
            print(f"GitHub Engine initialized. Authenticated to {self.repo_name}")
        else:
            self.gh = Github()
            print(f"GitHub Engine initialized. WARNING: Unauthenticated mode (Strict rate limits apply).")   