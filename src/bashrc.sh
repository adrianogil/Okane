
if [ -z "$OKANE_PYTHON_PATH" ]
then
    export OKANE_PYTHON_PATH=$OKANE_DIR/python
    export PYTHONPATH=$OKANE_PYTHON_PATH:$PYTHONPATH
fi

function okane()
{
    python3 -m okane $*
}
alias ok="okane"

function okanes()
{
    python3 -m okane $* --porcelain | less
}

function okane-add-fuzzy-account()
{
    target_account_id=$(okane -la | default-fuzzy-finder | awk '{print $2}')
    python3 -m okane $* -ac ${target_account_id}
}
alias ok-ac="okane-add-fuzzy-account"
