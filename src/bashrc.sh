
if [ -z "$OKANE_PYTHON_PATH" ]
then
    export OKANE_PYTHON_PATH=$OKANE_DIR/python
    export PYTHONPATH=$OKANE_PYTHON_PATH:$PYTHONPATH
fi

function okane()
{
    python3 -m okane $*
}

function okanes()
{
    set-okane-python-path

    python3 -m okane $* --porcelain | less
}