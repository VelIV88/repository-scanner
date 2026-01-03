#!/bin/bash

REPOS_DIR="/workspace/repositories"
REPORTS_DIR="/workspace/reports"
repos_names=$(ls $REPOS_DIR) 

if [ $# -eq 0 ]; then
    for name in $repos_names;do
            gitleaks detect \
            -s $REPOS_DIR/$name \
            -r $REPORTS_DIR/$name.json
            python3 /workspace/reports_processing.py $REPOS_DIR/$name $REPORTS_DIR/$name.json
    done
else
    gitleaks detect \
    -s $REPOS_DIR/$1 \
    -r $REPORTS_DIR/$name.json
    python3 /workspace/reports_processing.py $REPOS_DIR/$name $REPORTS_DIR/$name.json
fi