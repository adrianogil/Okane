alias okane='python2 "'$OKANE_DIR'"/src/okane.py'

function okanes()
{
    python2 $OKANE_DIR/src/okane.py $* --porcelain | less
}