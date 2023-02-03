#!/usr/bin/bash
echo "running as $(whoami) at $PWD"
git pull
poetry update
