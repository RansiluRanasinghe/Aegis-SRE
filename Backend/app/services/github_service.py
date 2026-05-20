import os
from github import Github
from github.GithubException import GithubException
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO", "RansiluRanasinghe/Aegis-SRE") 

if GITHUB_TOKEN:
    github_client = Github(GITHUB_TOKEN)
    print("GitHub Engine initialized. Authenticated Mode.")
else:
    github_client = Github()
    print("GitHub Engine initialized. WARNING: Unauthenticated mode (Read-only).")

def get_recent_commits(limit: int = 5) -> str:

    try:
        repo = github_client.get_repo(GITHUB_REPO)
        commits = repo.get_commits()[:limit]
        
        commit_log = ""
        for commit in commits:
            commit_log += f"- [{commit.sha[:7]}] {commit.commit.author.name}: {commit.commit.message.split('\n')[0]}\n"
            
        return commit_log if commit_log else "No recent commits found."
    except Exception as e:
        return f"Error fetching commits: {str(e)}"

def create_incident_ticket(title: str, body: str) -> str:

    if not GITHUB_TOKEN:
        return "Error: GITHUB_TOKEN is missing. Aegis cannot write to the repository."
    
    try:
        repo = github_client.get_repo(GITHUB_REPO)
        
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