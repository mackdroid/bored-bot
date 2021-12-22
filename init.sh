#!/usr/bin/fish
if test -z "$VIRTUAL_ENV"
    source ./venv/bin/activate.fish
end
./main.py
