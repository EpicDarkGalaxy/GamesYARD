# Contributing to GamesYARD

Thanks for your interest in contributing! Below are the minimal steps to get started and a short checklist for pull requests.

Getting started

1. Fork the repository and clone your fork:

```bash
git clone https://github.com/<your-username>/GamesYARD.git
cd GamesYARD
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows (PowerShell)
# .\venv\Scripts\Activate.ps1
# Windows (cmd)
# venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the app locally to verify your change:

```bash
python app.py
```

Coding guidelines

- Target Python 3.10+.
- Use descriptive commit messages and small focused PRs.
- Keep UI and core logic separated (src/ui/ vs src/core/).

Tests and checks

- There are no automated tests yet; running the app and manual verification is fine for most changes.

How to submit a change

1. Create a feature branch: `git checkout -b my-fix-or-feature`
2. Make your changes and commit them.
3. Push the branch to your fork and open a Pull Request against `EpicDarkGalaxy/GamesYARD:main`.

Pull request checklist

- [ ] The change is small and focused.
- [ ] I updated the README or other docs when appropriate.
- [ ] I ran the application to verify there are no obvious runtime errors.

If you're new and want a starter task, check the issues labeled `good-first-issue`.

Thank you — contributions are welcome!