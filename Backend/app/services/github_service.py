import os
from github import Github
from github.GithubException import GithubException
from app.core.config import settings

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO", "repo-owner/repo-name")

if GITHUB_TOKEN:
    gitub_client = Github(GITHUB_TOKEN)
    print("GitHub Engine initialized. Authenticated Mode.")
else:
    gitub_client = Github()
    print("GitHub Engine initialized. WARNING: Unauthenticated mode (Read-only).")    

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

    def get_recent_commits(self, limit: int = 15) -> str:

        try:
            repo = self.gh.get_repo(self.repo_name)
            commits = repo.get_commits()[:limit]

            content_str =  f"Live Architecture Context from {self.repo_name}\n\nRecent Commits:\n"

            for commit in commits:
                hash_short = commit.sha[:7]
                author = commit.commit.author.name

                msg = commit.commit.message.split("\n")[0]
                content_str = f"- [{hash_short}] {author}: {msg}\n"

            return content_str

        except GithubException as e:
            error_msg = e.data.get('message', str(e))
            print(f"GitHub API Error: {error_msg}")
            return f"Error loading repository context: {error_msg}"
        except Exception as e:
            return f"System Error reading GitHub: {str(e)}"
        
    def create_incident_issue(title: str, body: str) -> str:

        if not GITHUB_TOKEN:
            return "Error: GITHUB_TOKEN is missing. Aegis cannot write to the repository."

        try:
            repo = gitub_client.get_repo(GITHUB_REPO)

            issue = repo.create_issue(
                title=title,
                body=body,
                labels=["bug", "aegis-sre-auto", "critical"]
            )

            return issue.html_url
        except GithubException as e:
            return f"GitHub API Error: {e.data.get('message', str(e))}"
        except Exception as e:
            return f"Internal Error: {str(e)}"  

gitub_engine = GitHubService()                     