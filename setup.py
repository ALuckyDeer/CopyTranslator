from cx_Freeze import setup, Executable
import sys
base = 'WIN32GUI' if sys.platform == "win32" else None


executables = [Executable("CopyTrans.py", base=base,icon = "logo.ico")]

packages = []
include_files=['logo.png','logo.ico']
options = {
    'build_exe': {
        'packages':packages,
        'include_files': include_files
    },

}

setup(
    name = "CopyTrans",
    options = options,
    version = "1.0",
    description = 'CopyTranslater By XingKongXiaDeFeng!',
    executables = executables
)


