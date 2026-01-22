---
name: repo-structure-improver
description: Guide for analyzing, proposing, and implementing improvements to repository structure. Use this skill when the user wants to reorganize, refactor, clean up, or optimize the file structure of a codebase.
---

# Repo Structure Improver

This skill guides you through the process of improving a repository's structure. The goal is to make the codebase more readable, organized, and minimal while ensuring structural consistency.

## Phase 1: Analysis

Before making any changes, you must understand the current state of the repository.

1.  **Map Current State**: List all files and directories (use `list_dir`).
2.  **Infer Intent**: Analyze the codebase to understand its architectural purpose (e.g., MVC, Microservices, Monolith). Read key files (`README.md`, `setup.py`, `package.json`, main entry points).
3.  **Identify Issues**: Look for:
    *   **Inconsistent Naming**: Mixed cases, unclear names.
    *   **Misplaced Files**: Files that don't belong in their current directories.
    *   **Deep Nesting**: Unnecessarily deep directory structures.
    *   **Duplicates**: Multiple config files (e.g., multiple `requirements.txt`), duplicate utility scripts.
    *   **Redundancy**: Empty directories, unused files, deprecated code.
    *   **Tangle**: Circular dependencies or spaghetti code structure.

## Phase 2: Proposal

You **MUST** create a comprehensive plan and get user approval before touching any files.

1.  **Create Artifact**: Create a file named `refactoring_plan.md`. This artifact will evolve as you refine the plan.
2.  **Define Changes**: For every proposed change, specify:
    *   **Current Location**: `path/to/old/file`
    *   **New Location**: `path/to/new/file`
    *   **Reasoning**: Why this move improves structure (e.g., "Grouped all adapters together").
3.  **Handle Duplicates & Redundancy (CRITICAL)**:
    *   **Identify**: Explicitly list all duplicate files (e.g., `backend/requirements.txt` vs `root/requirements.txt`) and empty/redundant files.
    *   **Propose Action**: Suggest whether to **MERGE**, **DELETE**, or **KEEP**.
    *   **Justification**: You **MUST** provide a solid reason for every merge or deletion.
    *   **Permission**: You **MUST** explicitly ask the user for permission to perform these destructive actions.
4.  **Visualize New Structure (REQUIRED)**:
    *   You **MUST** include a visual representation of the proposed new file tree in the `refactoring_plan.md`.
    *   Use a tree-like format to show the hierarchy clearly.
    *   Highlight NEW directories and MOVED files.
5.  **Review**: Present `refactoring_plan.md` to the user via `notify_user`. Do not proceed until approved.

## Phase 3: Implementation

Once the plan is approved, execute the changes carefully.

1.  **Safety First**: Ensure your environment is clean (no uncommitted changes if possible, though you cannot enforce this, you can check).
2.  **Move Files**: Use `run_command` to move files (e.g., `mv` or `git mv` if it's a git repo).
    *   *Tip*: Create new directories *before* moving files into them.
3.  **Handle Merges/Deletions**:
    *   If merging files (e.g., requirements), READ both files, combine contents logically, WRITE the merged file, then DELETE the old ones.
    *   If deleting files, ensure you have user permission from Phase 2.
4.  **Update References (CRITICAL)**:
    *   Moving a file breaks imports. You **MUST** fix them immediately.
    *   **Search**: Use `grep_search` to find all import statements referencing the moved files.
    *   **Replace**: Use `replace_file_content` or `multi_replace_file_content` to update import paths.
    *   *Check*: Don't forget non-code references (string paths in config files, documentation links).
5.  **Clean Up**: Remove any now-empty directories.

## Phase 4: Verification

Ensure the refactoring didn't break the application.

1.  **Consistency Check**:
    *   Verify all files are where they should be (`list_dir`).
    *   Check for broken imports again (run a linter if available, or spot check key files).
2.  **Automated Testing**:
    *   Run the project's build command (e.g., `npm run build`, `python setup.py build`).
    *   Run the project's test suite (e.g., `npm test`, `pytest`).
    *   *If tests fail*: Stop. Analyze the error. It is likely an import path issue you missed. Fix it and re-run tests.
3.  **Final Report**: Create/Update `walkthrough.md` summarizing the changes made and the verification results.

# Guiding Principles

*   **Minimalism**: Fewer directories are often better. Don't over-engineer the folder structure.
*   **Readability**: A new developer should understand the project layout in 5 seconds.
*   **Organization**: Keep related things together (Cohesion). Separate unrelated things (Coupling).
*   **Safety**: Never delete code without being 100% sure and having user approval.
