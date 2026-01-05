name: Sync BotLi Python Files

on:
  workflow_dispatch:  # Run manually
  push:
    branches:
      - main

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout your repo
        uses: actions/checkout@v4
        with:
          fetch-depth: 0   # so we can rebase/pull cleanly

      - name: Clone Torom/BotLi
        run: |
          git clone --depth 1 https://github.com/Torom/BotLi temp_BotLi

      - name: Copy over only .py files
        run: |
          rsync -av --include='*/' --include='*.py' --exclude='*' temp_BotLi/ ./

      - name: Configure Git
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"

      - name: Commit changes
        run: |
          git add -u
          git add *.py || true
          git commit -m "Sync .py files from Torom/BotLi" || echo "No changes to commit"

      - name: Pull remote changes (avoid rejected push)
        run: |
          git pull --rebase origin main || true

      - name: Push changes
        run: |
          git push origin main
