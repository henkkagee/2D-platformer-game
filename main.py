import sys
from PyQt5.QtWidgets import QApplication
from GUI import MainGUI
from PyQt5 import QtCore
import traceback

import inspect
from PyQt5 import Qt

vers = ['%s = %s' % (k,v) for k,v in vars(Qt).items() if k.lower().find('version') >= 0 and not inspect.isbuiltin(v)]
print('\n'.join(sorted(vers)))
print(sys.version)

"""def excepthook(type_, value, traceback_):
    traceback.print_exception(type_, value, traceback_)
    QtCore.qFatal('')
sys.excepthook = excepthook"""

# Back up the reference to the exceptionhook
"""sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys.excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook"""

def main():
    app = QApplication(sys.argv)
    gui = MainGUI()
    return app.exec_()

if __name__ == "__main__":
    main()
    

