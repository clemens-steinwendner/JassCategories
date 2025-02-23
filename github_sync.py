from github import Github
import pandas as pd
import os
from datetime import datetime
import time

class GitHubSync:
    def __init__(self, token, repo_name):
        """Initialize GitHub sync with token and repository name"""
        try:
            self.github = Github(token)
            # Get the authenticated user
            user = self.github.get_user()
            # Try to get the repository
            try:
                self.repo = user.get_repo(repo_name)
            except Exception as e:
                # If repo doesn't exist, create it
                self.repo = user.create_repo(repo_name, description="Jass Categories Data Collection", private=True)
        except Exception as e:
            raise Exception(f"GitHub initialization failed: {str(e)}")
            
        self.local_cache = []
        self.last_sync_time = time.time()
        self.sync_interval = 300  # sync every 5 minutes

    def add_categorization(self, cards, category, username):
        """Add a new categorization to the local cache"""
        row = cards + [category, username, datetime.now().isoformat()]
        self.local_cache.append(row)
        
        # Try to sync if enough time has passed
        if time.time() - self.last_sync_time > self.sync_interval:
            self.sync_to_github()

    def sync_to_github(self):
        """Sync local cache to GitHub"""
        if not self.local_cache:
            return

        try:
            # Create DataFrame from cache
            columns = [f"num{i}" for i in range(9)] + ["trumpf", "username", "timestamp"]
            df = pd.DataFrame(self.local_cache, columns=columns)

            # Try to get existing file content
            try:
                file = self.repo.get_contents("categorizations.csv")
                existing_content = file.decoded_content.decode()
                existing_df = pd.read_csv(pd.StringIO(existing_content))
                df = pd.concat([existing_df, df], ignore_index=True)
            except:
                pass  # File doesn't exist yet

            # Convert DataFrame to CSV string
            csv_content = df.to_csv(index=False)

            # Create or update file on GitHub
            message = f"Update categorizations - {len(self.local_cache)} new entries"
            if 'file' in locals():
                self.repo.update_file(
                    "categorizations.csv",
                    message,
                    csv_content,
                    file.sha
                )
            else:
                self.repo.create_file(
                    "categorizations.csv",
                    message,
                    csv_content
                )

            # Clear cache after successful sync
            self.local_cache = []
            self.last_sync_time = time.time()
            return True
        except Exception as e:
            print(f"Error syncing to GitHub: {e}")
            return False

    def force_sync(self):
        """Force a sync to GitHub regardless of the timer"""
        return self.sync_to_github() 