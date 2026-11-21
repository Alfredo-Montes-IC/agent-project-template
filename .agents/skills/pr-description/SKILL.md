---
name: pr-description
description: Writes GitHub pull request descriptions in a fixed What/Why/Changes format. Use when the user is creating or writing a PR, or asks to summarize branch changes for a pull request.
---

# PR Description Writer

Write a GitHub pull request description for the changes between a source branch and a destination branch. The user types the branch names; do not use multiple-choice questions.

## Steps

1. **Gather context.** In the repository, run:
   - `git branch --show-current` for the current branch.
   - `git for-each-ref --sort=-committerdate --format='%(refname:short)' refs/heads refs/remotes` for branches, most recently updated first. Drop symbolic remote HEAD refs such as `origin/HEAD`. Keep local and remote-qualified names distinct (for example, `main` and `origin/main`), and use the typed ref unchanged in step 3.

2. **Ask the user to type the answers.** Do not use AskUserQuestion or any selection tool. Send one chat message asking for:
   - **Source branch:** default to the current branch, shown in the prompt.
   - **Destination branch** (the branch the PR merges into): list the likely candidates (`develop`, `main`, `master`, `stage`, whichever exist) as a hint, and name the suggested default (closest by `git merge-base`). Never assume `main`.

   Then wait for the user's typed reply. Skip any question the user already answered in their prompt. If the reply is empty or the user says "default", use the suggested values. If source and destination are the same branch, ask again for a different destination. Verify the typed names exist with `git rev-parse --verify <name>` and re-ask if not.

3. **Analyze the changes.** Run `git diff <destination>...<source> --ignore-cr-at-eol` to see all changes the source branch adds on top of the destination. The `--ignore-cr-at-eol` flag keeps CRLF/LF line-ending noise out of the diff. Also run `git log <destination>..<source> --oneline` to see the commits. If the diff is large, start with `--stat`.

4. **Write the description.** Use exactly this format, with GitHub syntax applied (see step 5):

   ```markdown
   ## What
   One sentence explaining what this PR does.

   ## Why
   Brief context on why this change is needed.

   ## Changes
   - Bullet points of specific changes made.
   - Group related changes together.
   - Mention any files deleted or renamed.
   ```

5. **Apply GitHub formatting.** Use GitHub-flavored Markdown. Link issues with `Closes #123` / `Fixes #123` and cross-repo as `owner/repo#123`. Mention people with `@username`. Use task lists (`- [ ]`) only if the diff has follow-ups.
   - Only add issue links if an issue number appears in a branch name or commit message. Never invent one.

6. **Save and present the file.** Write the result to `PR_DESCRIPTION.md` at the repository root, then show it with the host's file-presenting tool if available; otherwise provide a supported file link or the repository-relative path in chat. Do not commit it.
   - Line 1 is the title as a `#` heading, followed by a blank line, then the What/Why/Changes sections.
   - If `PR_DESCRIPTION.md` already exists, overwrite it.
   - Keep the closing message to one or two sentences. Do not paste the full description again in chat.

7. **Generate a title.** Write a concise, descriptive PR title in the imperative mood (e.g. "Add pr-description skill"). Use it as the `#` heading in the file, and repeat it as the last line of the chat reply so it can be copied into the title field.