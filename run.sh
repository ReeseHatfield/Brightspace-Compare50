#!/bin/bash


if [[ -d "venv" ]]; then
    python3 -m venv venv
fi

source venv/bin/activate

pip install -r requirements.txt

clear

python3 -m d2l-cs50 $@


rm *.log

deactivate