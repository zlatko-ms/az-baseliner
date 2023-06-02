#!/bin/bash
BASEDIR=$(dirname $0)
source=main
target=$(git rev-parse --abbrev-ref HEAD)
x=$( "$BASEDIR/rebase_workflow.sh" -s $source -t $target)  
