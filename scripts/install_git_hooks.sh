#!/bin/sh
set -eu

git config core.hooksPath .githooks
chmod +x .githooks/pre-commit
echo "Installed git hooks from .githooks"
