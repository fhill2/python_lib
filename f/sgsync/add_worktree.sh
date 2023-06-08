#!/usr/bin/sh
if [ $(git worktree list | wc -l) -lt 2 ]; then git worktree add wt; fi
# current_branch=$(git rev-parse --abrev-ref HEAD) 
 # echo "less  than 1"
# fi
