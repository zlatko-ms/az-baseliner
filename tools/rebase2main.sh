BASEDIR=$(dirname $0)
target=main
source=$(git rev-parse --abbrev-ref HEAD)
x=$( "$BASEDIR/rebase_workflow.sh" -s $source -t $target)  