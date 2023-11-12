
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

function okane-update-register()
{
    target_register_id=$(okane -l --oneline $* | default-fuzzy-finder | tr '(' ' ' | tr ')' ' ' | awk '{print $1}')
    okane -u ${target_register_id}
}

function okane-update-category()
{
    target_category_id=$(okane -lc --oneline $* | default-fuzzy-finder | tr '-' ' ' | tr '[' ' ' | tr ']' ' ' | awk '{print $1}')
    okane -uc ${target_category_id}
}