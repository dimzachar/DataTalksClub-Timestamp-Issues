import requests
from bs4 import BeautifulSoup
from github import Github


class GitHubUtility:
    """
    Utility class to interact with GitHub for specific repository operations.
    """

    def __init__(self, access_token, repo_name):
        """
        Initialize the GitHub utility.

        :param access_token: GitHub API access token
        :param repo_name: Name of the GitHub repository
        """
        self.g = Github(access_token)
        print(f"Attempting to access repo: {repo_name}")
        self.repo = self.g.get_repo(repo_name)
        self.processed_issues = set()
        print("Successfully accessed repo")

    def get_video_titles_from_issues(self, page=1):
        """
        TODO: Use Github API instead of webscrape (??)
        Fetch video titles from GitHub issues.

        :param page: Page number for GitHub issues pagination
        :return: List of video titles
        """
        print(f"Fetching video titles from issues, page {page}")
        issues_url = f"https://github.com/{self.repo.full_name}/issues?page={page}&q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc"

        try:
            response = requests.get(issues_url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"An error occurred while fetching issues: {e}")
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        issue_titles = [
            el.text.strip() for el in soup.find_all("a", class_="Link--primary")
        ]
        video_titles = [
            title.replace("Timecodes for ", "").replace('"', '')
            for title in issue_titles
            if title.startswith("Timecodes for ")
        ]
        print(f"Fetched {len(video_titles)} video titles")
        return video_titles

    def is_already_processed(self, issue_title):
        """
        Check if the issue has already been processed.

        :param issue_title: Title of the issue to check
        :return: True if already processed, False otherwise
        """
        if issue_title in self.processed_issues:
            return True

        issues = self.repo.get_issues(state="open")
        for issue in issues:
            if issue.title == issue_title:
                for comment in issue.get_comments():
                    if comment.user.login == self.g.get_user().login:
                        self.processed_issues.add(issue_title)
                        return True
        return False

    def add_issue_comment_with_confirmation(
        self, issue_titles, comment_body, confirm_prompt=True
    ):
        """
        TODO: Modularize Code (??)
        Add a comment to a GitHub issue with optional confirmation.

        :param issue_titles: List of issue titles to add comments to
        :param comment_body: Text to include in the comment
        :param confirm_prompt: Whether to prompt user for confirmation before adding comment
        """
        print("Entering add_issue_comment_with_confirmation function")
        issues = self.repo.get_issues(state="open")
        for issue in issues:
            print(f"Checking issue: {issue.title}")
            if issue.title.strip() in issue_titles:
                print(f"\nAdding comment to issue '{issue.title}':\n")
                print(comment_body)
                if confirm_prompt:
                    proceed = input("\nProceed with commit? [y/N]: ")
                else:
                    proceed = 'y'

                if proceed.lower() == "y":
                    issue.create_comment(comment_body)
                    print("Comment added.")
                else:
                    print("Skipped.")
                break
