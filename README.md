Contributors: @zlwaterfield, @raquelmsmith

# PR Checker

`pr-checker` is a CLI tool to check the status of pull requests on GitHub for a specified user or team. It's great for seeing what work was completed in the last 7 days (or custom time window), and what work remains open.

## Features

- Initialize configuration with GitHub username, token, team usernames, and repositories.
- Update specific parts of the configuration such as GitHub token, username, team usernames, and repositories.
- Check the status of open and closed pull requests for specified date ranges.

## Installation

Install the package using `pip`:

```sh
pip install pr-checker
```

## Prerequisites

You'll need to create a personal access token for Github. Visit the [Fine-grained personal access tokens](https://github.com/settings/tokens?type=beta) page in your GitHub settings. Create a token with `read` access to all the repositories you are wanting to check.

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
pr-checker --update-config --set-token NEW_TOKEN
```

#### Update GitHub username

```sh
pr-checker --update-config --set-username NEW_USERNAME
```

#### Update Team Usernames

```sh
pr-checker --update-config --set-team "user1,user2"
```

#### Update repositories

```sh
pr-checker --update-config --set-repos "Org1/repo1, Org2/repo2"
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
- `--update-config`: Update the configuration.
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
