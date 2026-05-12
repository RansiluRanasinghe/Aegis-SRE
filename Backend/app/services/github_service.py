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