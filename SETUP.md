# GitHub Profile Setup — Shivam Kanala

1. On GitHub, create a **public** repository named `shivamkanala-45` (exactly your username). If it exists, use that repository instead.
2. Upload **all** contents of this package to the root of the repository, including the hidden `.github` folder. Keep the directory structure unchanged.
3. In repository **Settings → Actions → General → Workflow permissions**, select **Read and write permissions**, then save. If an organization policy prevents this, ask an administrator.
4. Open **Actions → Update profile animations and stats → Run workflow**. Wait for the run to finish.
5. Refresh `https://github.com/shivamkanala-45` to see the animated shooter GIF and generated summary cards. The workflow also runs every Monday.
6. Replace the placeholder project details/links with your published projects. Add LinkedIn/email/portfolio links only if you want them public.

## Troubleshooting

- **Missing GIF or summary cards:** The assets are generated only after the first successful workflow run; check Actions logs.
- **403 when pushing:** Confirm Actions workflow has read/write permissions and the default branch is `main`.
- **GraphQL error:** The workflow uses `secrets.GITHUB_TOKEN`. Ensure Actions is enabled. Private contributions may not be included.
- **Summary card action fails:** Check its current marketplace documentation; external actions can change.
- **Remote images broken:** Some image hosting services have outages/rate limits. These do not affect the locally generated shooter GIF.

## Local development

`python -m pip install Pillow`

To run the shooter script locally, set `GH_USERNAME` and a GitHub token in `GH_TOKEN` with permission to read your contribution calendar. Do not commit tokens to Git.
