#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime, timedelta
from typing import Literal, Optional

import requests

CONFIG_FILE_PATH = os.path.join(os.path.expanduser("~"), ".pr_checker_config.json")


def load_config():
    if os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, 'r') as f:
            return json.load(f)
    else:
        return {
            "my_username": "",
            "token": "",
            "team_usernames": []
        }

def update_config(my_username=None, token=None, team_usernames=None, repos=None):
    config = load_config()

    if my_username is not None:
        config["my_username"] = my_username
    if token is not None:
        config["token"] = token
    if team_usernames is not None:
        config["team_usernames"] = [username.strip() for username in team_usernames.split(",")]
    if repos is not None:
        config["repos"] = [repo.strip() for repo in repos.split(",")]

    save_config(config)
    print("Configuration updated!")

def save_config(config):
    with open(CONFIG_FILE_PATH, 'w') as f:
        json.dump(config, f, indent=4)


def init_config():
    config = load_config()

    config["my_username"] = input("Enter your GitHub username: ")
    config["token"] = input("Enter your GitHub token: ")
    team_usernames = input("Enter your team usernames (comma-separated): ")
    config["team_usernames"] = [username.strip() for username in team_usernames.split(",")]
    repos = input("Enter the repositories you want to check (comma-separated, eg PostHog/posthog): ")
    config["repos"] = [repo.strip() for repo in repos.split(",")]

    save_config(config)
    print("Configuration saved!")


def handle(status: Literal["closed", "open", None] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, who: Optional[Literal["me", "team"]] = None):
    config = load_config()

    usernames = []
    my_username = config["my_username"]
    team_usernames = config["team_usernames"]
    if who == "me":
        usernames = [my_username]
    elif who == "team" or who is None:
        usernames = team_usernames + [my_username]
    token = config["token"]

    # Repositories to check
    repos = config["repos"]

    # Headers for GitHub API requests
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }

    today = datetime.today()
    if not start_date:
        start_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = today.strftime("%Y-%m-%d")

    print(f"\n\nPRs for {', '.join(usernames)} between {start_date} and {end_date}")

    # Process each repo
    for repo in repos:
        print(f"\n - \033[1m\u001b[36m{repo}\u001b[0m\033[0m")

        # Get merged PRs
        if status in ["closed", None]:
            merged_prs = get_prs(repo, "closed", headers, start_date, usernames)
            for pr in merged_prs:
                if pr['user']['login'] in usernames or (pr['assignee'] and pr['assignee']['login'] in usernames):
                    merged_at = pr.get("merged_at")
                    if merged_at:
                        merged_date = datetime.strptime(merged_at, "%Y-%m-%dT%H:%M:%SZ").date()
                        if datetime.strptime(start_date, "%Y-%m-%d").date() <= merged_date <= datetime.strptime(end_date, "%Y-%m-%d").date():
                            print(f"   - \u001b[35m[merged:{merged_date}]\u001b[0m \u001b[34m@{pr['user']['login']}\u001b[0m -- \x1B]8;;{pr['html_url']}\x1B\\{pr['title']}\x1B]8;;\x1B\\")

        # Get open PRs
        if status in ["open", None]:
            open_prs = get_prs(repo, "open", headers, start_date, usernames)
            for pr in open_prs:
                if pr['user']['login'] in usernames or (pr['assignee'] and pr['assignee']['login'] in usernames):
                    print(f"   - \u001b[33m[open]\u001b[0m \u001b[34m@{pr['user']['login']}\u001b[0m -- \x1B]8;;{pr['html_url']}\x1B\\{pr['title']}\x1B]8;;\x1B\\")

# Function to get PRs for a given repo
def get_prs(repo, state, headers, start_date, usernames):
    url = f"https://api.github.com/repos/{repo}/pulls"
    page = 1
    results = []
    get_next_page = True
    sort = "created" if state == "open" else "updated"

    while get_next_page:
        params = {
            "state": state,
            "sort": "created",
            "direction": "desc",
            "per_page": "100",
            "page": page
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        for pr in response.json():
            if pr['user']['login'] in usernames or (pr['assignee'] and pr['assignee']['login'] in usernames):
                results.append(pr)
        if response.json()[-1]:
            last_pr_date = datetime.strptime(response.json()[-1]['created_at'], "%Y-%m-%dT%H:%M:%SZ").date()
            if last_pr_date < datetime.strptime(start_date, "%Y-%m-%d").date():
                get_next_page = False
            page += 1
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Script to check PR statuses on GitHub"
    )
    parser.add_argument("--status", required=False, type=str, help="Status of the PRs, closed or open. Leave blank for both.")
    parser.add_argument("--start-date", required=False, type=str, help="Start date for the PRs. Defaults to 7 days ago.")
    parser.add_argument("--end-date", required=False, type=str, help="End date for the PRs. Defaults to today.")
    parser.add_argument("--who", required=False, type=str, help="Who to check PRs for. me or team. Leave blank for team (includes me).")
    parser.add_argument("--init", action="store_true", help="Initialize configuration")
    parser.add_argument("--update-config", action="store_true", help="Update configuration")
    parser.add_argument("--set-username", required=False, type=str, help="Set GitHub username")
    parser.add_argument("--set-token", required=False, type=str, help="Set GitHub token")
    parser.add_argument("--set-team", required=False, type=str, help="Set team usernames (comma-separated)")
    parser.add_argument("--set-repos", required=False, type=str, help="Set repositories to check (comma-separated)")

    args = parser.parse_args()

    if args.init:
        init_config()
    elif args.update_config:
        update_config(args.set_username, args.set_token, args.set_team, args.set_repos)
    else:
        status = args.status or None
        start_date = args.start_date or None
        end_date = args.end_date or None
        who = args.who or None
        handle(status, start_date, end_date, who)

if __name__ == "__main__":
    main()