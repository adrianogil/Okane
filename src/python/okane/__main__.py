#!/usr/bin/env python
import sys, os

import utils

from okane.okanecontroller import OkaneController
import okane.utils.logsystem as logsystem


if '--debug' in sys.argv:
    print("Debug mode activated")
    logsystem.printlog.debug_mode = True

# Open Connection
okane_directory = os.environ.get('OKANE_DIR', '')

if not okane_directory:
    # Let's assume we are running directly from the repo folder
    okane_directory = os.getcwd().replace('src/python', 'src')

controller = OkaneController(okane_directory)
controller.run_cli()
