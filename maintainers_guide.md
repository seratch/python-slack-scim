# Maintainers Guide

This document describes tools, tasks and workflow that one needs to be familiar with in order to effectively maintain this project. If you use this package within your own software as is but don't plan on modifying it, this guide is **not** for you.

## Contribution

Your contributions are always welcome! Before submitting a pull request, verify your code works with Slack SCIM APIs.

```bash
export SLACK_SDK_TEST_GRID_ORG_ADMIN_USER_TOKEN=xoxp-***
SLACK_SCIM_TEST_MODE=prod python setup.py test
```

## Deployment

```bash
# https://packaging.python.org/guides/using-testpypi/
pip install twine wheel
rm -rf dist/
python setup.py sdist bdist_wheel
twine check dist/*

# Testing
twine upload --repository testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ slack-scim

# Deployment
twine upload dist/*
```

