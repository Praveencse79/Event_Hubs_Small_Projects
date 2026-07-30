Check if Git is installed: git --version
Configure Git :- 
               git config --global user.name "Praveen Kumar"
               git config --global user.email "praveen@gmail.com"
git config: Used to configure Git settings.
--global: Applies the setting to all repositories on your computer.
user.name: Your display name in commits.
user.email: Email associated with your commits.
git config --list: Shows all current Git settings.
Create a Folder: mkdir AzureProject
Move into it: cd AzureProject
Initialize Git: git init
Git creates a hidden .git folder.
AzureProject
│
├── .git
├── README.md
The .git folder stores the repository history and metadata.
Check Status: git status
Add File: git add README.md AND git add .
git add: Moves changes from the Working Directory to the Staging Area.
Commit: git commit -m "Initial Commit"
git commit: Saves a snapshot of your staged changes.
-m : Adds a commit message.
View History: git log
Create a Branch : git branch development
List branches: git branch
Switch Branch: git checkout development
Or create and switch in one command: git checkout -b feature/adf
Merge Branch: git checkout main
Merge: git merge feature/adf :- This brings the changes from feature/adf into main.
Clone Repository: git clone https://github.com/username/project.git :- Downloads an existing GitHub repository to your local machine.
Push to GitHub:- git push origin main 
push: Uploads commits.   origin: Default name for the remote GitHub repository. main: Branch to push.
Pull Latest Code: git pull origin main   :- Downloads and merges the latest changes from GitHub.
See Differences: git diff


