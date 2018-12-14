function set-okane-python-path()
{
    if [ -z "$OKANE_PYTHON_PATH" ]
    then
        export OKANE_PYTHON_PATH=$OKANE_DIR/src
        export PYTHONPATH=$OKANE_PYTHON_PATH:$PYTHONPATH
    fi
}

function okane()
{
    set-okane-python-path

    python2 $OKANE_DIR/okane.py
}

function okanes()
{
    set-okane-python-path

    python2 $OKANE_DIR//okane.py $* --porcelain | less
}