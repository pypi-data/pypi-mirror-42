# DEV-README

## Dev setup with pip

```bash
python setup.py develop
```

## Visual Studio Code Setup
```json
///.vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File (Integrated Terminal)",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/venv/bin/gip",
            "args" : ["--gitlab-token=<token>",
                "--github-token=<token>",
                "--lock-file=./lib/.giplock.yml",
                "install", "-r", "tests/requirements.yml",
                "--upgrade=true"
            ],
            "console": "integratedTerminal"
        }
    ]
}
```

## Release
```bash
pip install -r test-requirements.txt
make -f build/Makefile clean
make -f build/Makefile build
make -f build/Makefile push
```