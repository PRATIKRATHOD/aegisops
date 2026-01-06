# Git Setup & Usage – AegisOps

This document explains how Git was configured and used for the AegisOps
project, including the purpose of each command executed.

The goal is to ensure clean version control, proper commit attribution,
and industry-standard Git practices.

---

## 1. Git Identity Configuration

Before creating any commits, Git user identity was configured globally.
This ensures that all commits are correctly attributed to the developer
and linked to the GitHub profile.

### Command Used
git config --global user.name "Pratik Rathod"

### What This Does
- Sets the author name for all Git commits
- This name appears in commit history and GitHub activity

### Command Used
git config --global user.email "github-email@example.com"

### What This Does
- Sets the email address for commits
- Must match the email used on GitHub for proper commit linking

### Verification Command
git config --global --list

### Purpose
- Verifies that `user.name` and `user.email` are correctly set
- Confirms Git identity is ready before committing code

---

## 2. Initializing Git Repository

The project directory was converted into a Git repository explicitly.

### Command Used
git init


### What This Does
- Creates a hidden `.git/` directory in the project root
- Enables version control for the entire project
- Marks the directory as a Git repository

---

## 3. Checking Repository Status

After initialization, repository status was checked to confirm Git is active.

### Command Used
git status

### What This Does
- Shows current branch (main)
- Lists tracked and untracked files
- Confirms whether commits exist or not

---

## 4. Adding Files to Staging Area

All project files were added to the Git staging area.

### Command Used
git add .

### What This Does
- Stages all files and directories under the project root
- Prepares files to be included in the next commit

---

## 5. Creating the First Commit

An initial commit was created to capture the foundational project state.

### Command Used
git commit -m "Initial project setup: incident creation and correlation"

### What This Does
- Creates the first snapshot of the project
- Stores incident creation, correlation logic, and documentation
- Establishes a clean commit history from the beginning

---

## 6. Branch Configuration (Optional Best Practice)

The default branch was set to `main` to follow modern Git standards.

### Command Used
git config --global init.defaultBranch main

### What This Does
- Ensures new repositories use `main` as the default branch
- Aligns with GitHub and enterprise standards

---

## Summary

Through these steps:
- Git was configured correctly before development
- The repository was initialized explicitly
- All changes were version-controlled from the start
- Commit history reflects a clean and professional workflow

This setup ensures the project is ready for collaboration,
code reviews, CI/CD pipelines, and open-source contribution.