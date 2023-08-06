# Gip

## Usage
```
gip --help

Usage: gip [OPTIONS] COMMAND [ARGS]...

   _______ __
  |     __|__|.-----.
  |    |  |  ||  _  |
  |_______|__||   __|
              |__|
  Gip is a language agnostic dependency manager
  which uses API calls to pull repositories.

  Enable autocomplete for Bash (.bashrc):   eval "$(_GIP_COMPLETE=source
  gip)"

  Enable autocomplete for ZSH (.zshrc):   eval "$(_GIP_COMPLETE=source_zsh
  gip)"

Options:
  --debug / --no-debug  Enable or disable debug mode. Default is disabled.
  --gitlab-token TEXT   Provide the private token for the Gitlab API.
                        Can be set as environment variable GIP_GITLAB_TOKEN
  --github-token TEXT   Provide the private token for the Github API.
                        Can be set as environment variable GIP_GITHUB_TOKEN
  --lock-file PATH      Provide the path to the lockfile, defaults to
                        .giplock.yml in the current working directory
  --version             Show the version and exit.
  --help                Show this message and exit.

Commands:
  install  Install dependencies, if already present just skips when version...
```


## Example of requirements.yml

```yaml
- name: ansible-role-plex  # directory name in destination directory
  repo: https://github.com/wilmardo/ansible-role-plex  # repository url
  type: github  # type: gitlab or github allowed
  version: 2.1.0  # version: tag, branch name or commit sha, defaults to master
  dest: lib/  # destination directory, defaults to current directory
```
