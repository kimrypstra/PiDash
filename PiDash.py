import os 
import sys

from git import Repo

import kivy
from kivy.app import App  
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from source.home.HomeView import HomeView

class PiDash(App): 
	def build(self):
		self.check_for_updates()
		return HomeView()

	def check_for_updates(self):
		script_path = os.path.realpath(__file__)
		script_dir = os.path.dirname(script_path)

		repo = Repo(script_dir)

		if repo.is_dirty(untracked_files=True):
			print("Uncommited changes, not updating")
			return

		branch = repo.active_branch.name 
		if branch != 'main':
			print("Not on main branch, not updating")
			return 

		origin = repo.remotes.origin
		origin.fetch()

		commits_behind = repo.iter_commits('HEAD..origin/main')
		if any(commits_behind):
			print(f"Behind by {length(commits_behind)}. Pulling...")
			origin.pull()
			os.execv(sys.executable, [sys.executable, script_path])
		else: 
			print("Up to date. Continuing execution...")

if __name__ == '__main__':
	PiDash().run()