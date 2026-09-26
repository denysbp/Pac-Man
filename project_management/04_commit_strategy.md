# Commit Strategy

## 1. Commit Organization

Git was used throughout the project to track the development process and maintain a history of the changes made by each team member.

Each developer committed their own changes while working on their assigned components.

The commit history was used to:

* Track the evolution of the project.
* Identify when features or fixes were introduced.
* Keep development work organized.
* Facilitate code review between team members.
* Provide a history of the project's development.

---

## 2. Development Workflow

The commit workflow followed the general development process:

```text
Implement change
      ↓
Test change
      ↓
Commit changes
      ↓
Other team member reviews
      ↓
Corrections if necessary
      ↓
Merge into main
```

Commits were therefore part of the development and review process rather than being created only at the end of the project.

---

## 3. Branches

The project used separate branches for development:

* `denys`
* `danilo`
* `main`

The `denys` and `danilo` branches were used for individual development.

The `main` branch was used as the integrated version of the project.

---

## 4. Commit History as Project Evidence

The Git history provides evidence of the project's development over time.

It allows the team to identify:

* Features that were implemented.
* Bugs that were fixed.
* Code that was restructured.
* Changes to the player and bot systems.
* Changes to the UI and game mechanics.
* Integration work between different components.

The commit history therefore served as an additional record of the actual progress of the project.

---

## 5. Review Before Integration

A change was not considered ready for integration simply because it had been committed.

The developer first tested the change, after which the other team member reviewed it.

When the change was considered ready, it was merged into `main`.

This workflow helped maintain a stable integrated version while allowing both developers to work independently.

---

## 6. Final Git State

The final repository contains the development history of the project across the individual development branches and the integrated `main` branch.

The Git history, together with the project documentation, provides evidence of how the project evolved from its initial structure to the completed version.
