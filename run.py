import os 
import sys

from git import Repo, exc

repo_path = os.path.dirname(os.path.realpath(__file__))
script_path = os.path.join(repo_path, "PiDash.py")

def check_for_updates():
		repo = Repo(repo_path)

		if repo.is_dirty(untracked_files=True):
			print("Uncommited changes, not updating")
			return

		branch = repo.active_branch.name 
		if branch != 'main':
			print("Not on main branch, not updating")
			return 

		origin = repo.remotes.origin
		try: 
			origin.fetch()

			commits_behind = repo.iter_commits('HEAD..origin/main')
			if any(commits_behind):
				print(f"Behind by {length(commits_behind)}. Pulling...")
				origin.pull()
			else:
				print("Already up to date. Continuing execution...")
		except (exc.GitError, OSError) as e: 
			print(f"Failed to update with error: {e}. \nContinuing launch.")

check_for_updates()

os.execv(sys.executable, [sys.executable, script_path])