# 🚀 Git & GitHub Commands Cheat Sheet

A quick reference for the most commonly used Git and GitHub commands.

---

# 📌 1. Check if Git is Installed

```bash
git --version
```

✅ Displays the installed Git version.

---

# ⚙️ 2. Configure Git (First Time Setup)

```bash
git config --global user.name "Praveen Kumar"
git config --global user.email "praveen@gmail.com"
```

### Explanation

* `git config` → Configures Git settings.
* `--global` → Applies settings to all repositories.
* `user.name` → Your display name in commits.
* `user.email` → Email associated with your commits.

### Verify Configuration

```bash
git config --list
```

Displays all configured Git settings.

---

# 📁 3. Create a New Project

### Create a Folder

```bash
mkdir AzureProject
```

### Move into the Folder

```bash
cd AzureProject
```

---

# 🔰 4. Initialize Git Repository

```bash
git init
```

Git creates a hidden `.git` folder.

```
AzureProject/
│
├── .git/
├── README.md
└── src/
```

The `.git` folder stores:

* Commit history
* Branch information
* Configuration
* Repository metadata

---

# 📋 5. Check Repository Status

```bash
git status
```

Shows:

* Modified files
* New files
* Deleted files
* Staged files
* Current branch

---

# ➕ 6. Add Files to Staging Area

### Add a Single File

```bash
git add README.md
```

or

```bash
git add Dim_table.py
```

### Add All Files

```bash
git add .
```

**What does `git add` do?**

Moves changes from the **Working Directory** to the **Staging Area**.

```
Working Directory
        │
        ▼
git add .
        │
        ▼
 Staging Area
```

---

# 💾 7. Commit Changes

### Commit Staged Files

```bash
git commit -m "Initial Commit"
```

Example:

```bash
git commit -m "Adding the new files for DimTable"
```

### Add & Commit Modified Files Together

```bash
git commit -am "Updating the files"
```

> **Note:** `git commit -am` works only for **tracked files**. It does **not** stage new files.

For new files, use:

```bash
git add .
git commit -m "Adding new files"
```

---

# 📜 8. View Commit History

```bash
git log
```

Short version:

```bash
git log --oneline
```

---

# 🌿 9. Create Branch

```bash
git branch development
```

Create another branch:

```bash
git branch feature2
```

---

# 📄 10. List All Branches

```bash
git branch
```

Example output:

```
* main
  development
  feature2
```

---

# 🔄 11. Switch Branch

```bash
git checkout development
```

---

# 🌟 12. Create and Switch Branch

```bash
git checkout -b feature/adf
```

or

```bash
git checkout -b feature2
```

This command:

* Creates a new branch
* Switches to it immediately

---

# 🔀 13. Merge Branches

Switch to the target branch:

```bash
git checkout main
```

Merge another branch:

```bash
git merge feature/adf
```

This brings all changes from `feature/adf` into `main`.

---

# 📥 14. Clone a Repository

```bash
git clone https://github.com/username/project.git
```

Downloads an existing GitHub repository to your local machine.

---

# ☁️ 15. Push Code to GitHub

Push the `main` branch:

```bash
git push origin main
```

Push another branch:

```bash
git push origin feature2
```

### Explanation

* `push` → Uploads commits
* `origin` → Remote GitHub repository
* `main` / `feature2` → Branch name

---

# 📥 16. Pull Latest Code

```bash
git pull origin main
```

Downloads and merges the latest changes from GitHub.

---

# 🔍 17. See File Differences

```bash
git diff
```

Shows changes before committing.

---

# 📌 Common Workflow

```
Create Folder
      │
      ▼
git init
      │
      ▼
Create Files
      │
      ▼
git status
      │
      ▼
git add .
      │
      ▼
git commit -m "Your message"
      │
      ▼
git push origin main
```

---

# ⭐ Daily Git Workflow

```bash
git status
git pull origin main
git checkout -b feature2
git add .
git commit -m "Added new feature"
git push origin feature2
```

---

# ⚡ Frequently Used Commands

| Command                       | Purpose                       |
| ----------------------------- | ----------------------------- |
| `git --version`               | Check Git version             |
| `git config --list`           | Show Git configuration        |
| `git init`                    | Initialize repository         |
| `git status`                  | Check repository status       |
| `git add .`                   | Stage all files               |
| `git add filename`            | Stage one file                |
| `git commit -m "message"`     | Commit staged changes         |
| `git commit -am "message"`    | Commit modified tracked files |
| `git log`                     | View commit history           |
| `git log --oneline`           | Compact commit history        |
| `git branch`                  | List branches                 |
| `git branch branch_name`      | Create a branch               |
| `git checkout branch_name`    | Switch branch                 |
| `git checkout -b branch_name` | Create & switch branch        |
| `git merge branch_name`       | Merge a branch                |
| `git clone URL`               | Clone repository              |
| `git push origin branch`      | Push code                     |
| `git pull origin branch`      | Pull latest changes           |
| `git diff`                    | Show differences              |

---

# 💡 Pro Tips

✅ Run `git status` frequently.

✅ Write meaningful commit messages.

✅ Create a feature branch for every new task.

✅ Pull the latest code before starting work.

✅ Push your code regularly as a backup.

---

# 🎯 Typical Feature Development Flow

```bash
git pull origin main

git checkout -b feature/customer-data

git status

git add .

git commit -m "Implemented customer data pipeline"

git push origin feature/customer-data
```

Happy Coding! 🚀
