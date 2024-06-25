# PR Checker

`pr-checker` is a CLI tool to check the status of pull requests on GitHub for a specified user or team. It supports initializing configuration, updating specific configuration parts, and checking the status of PRs.

## Features

- Initialize configuration with GitHub username, token, team usernames, and repositories.
- Update specific parts of the configuration such as GitHub token, username, team usernames, and repositories.
- Check the status of open and closed pull requests for specified date ranges.

## Installation

Install the package using `pip`:

```sh
pip install pr-checker
```

## Usage

### Initialize Configuration

The first time you use pr-checker, you need to initialize the configuration:

```sh
pr-checker --init
```

This will prompt you to enter your GitHub username, token, team usernames, and repositories to check.

### Update Configuration

You can update specific parts of the configuration as needed.

#### Update GitHub Token

```sh
pr-checker --update --set-token NEW_TOKEN
```

#### Update GitHub username

```sh
pr-checker --update --set-username NEW_USERNAME
```

#### Update Team Usernames

```sh
pr-checker --update --set-team "user1,user2"
```

#### Update repositories

```sh
pr-checker --update --set-repos "Repo1/repo1, Repo2/repo2"
```

### Check Pull Requests

You can check the status of pull requests using various options.

#### Default

No options checks PRs in all repos for both you and your team for the last 7 days.

```sh
pr-checker
```

#### Check Open Pull Requests for a Specific Date Range

```sh
pr-checker --status open --start-date 2022-01-01 --end-date 2022-01-31 --who me
```

#### Get only your pull requests

```sh
pr-checker --who team
```

### Arguments

- `--init`: Initialize the configuration.
- `--update`: Update the configuration.
  - `--set-username`: Set the GitHub username.
  - `--set-token`: Set the GitHub token.
  - `--set-team`: Set the team usernames (comma-separated).
  - `--set-repos`: Set the repositories to check (comma-separated).
- `--status`: Status of the PRs (open or closed). Leave blank for both.
- `--start-date`: Start date for the PRs.
- `--end-date`: End date for the PRs.
- `--who`: Who to check PRs for (me or team). Leave blank for team (includes me)

## License

This project is licensed under the MIT License.
