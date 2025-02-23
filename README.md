# Jass Categories Data Collection App

This application helps collect categorization data for Jass cards. The data is automatically synchronized with GitHub.

## Setup Instructions

1. Install required packages:
```bash
pip install PyGithub pandas numpy matplotlib
```

2. Create a GitHub Personal Access Token:
   - Go to GitHub Settings -> Developer Settings -> Personal Access Tokens
   - Create a new token with 'repo' permissions
   - Save this token somewhere safe - you'll need it when running the app

3. Run the application:
```bash
python CardRandomizer_test_real.py
```

4. When the app starts:
   - You'll be prompted for your GitHub token (first time only)
   - Enter your username (used to track who categorized what)
   - Start categorizing!

## How It Works

- The app shows you 9 cards at a time
- Categorize them using either the buttons or by typing the category code
- Data is automatically synced to GitHub every 5 minutes
- All data is also synced when you close the app
- Your progress is saved in the GitHub repository

## Categories

- Ei: Eichle
- Ro: Rose
- Se: Schelle
- Si: Schilte
- Oa: Obe abe
- Uu: Une ufe
- Soa: Slalom obe abe
- Suu: Slalom une ufe
- Sch: Schiebe!
