# Security

If a secret (like your Discord bot token) is accidentally committed:

- **Rotate it immediately** in the Discord Developer Portal.
- Do **not** add tokens to the repository. Use `.env` or GitHub Secrets instead.
- The repository contains a simple secret scanner (`tools/scan_secrets.sh`) and a CI job that runs it.

If you need help scrubbing secrets from git history, we can run `git-filter-repo` or BFG and force-push — note this rewrites history and will require all collaborators to re-clone.
