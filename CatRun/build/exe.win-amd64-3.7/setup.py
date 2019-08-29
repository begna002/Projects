import cx_Freeze
import os
from cx_Freeze import *

os.environ['TCL_LIBRARY'] = "C:\\Users\\Moti Begna\\AppData\\Local\\Programs\\Python\\Python37-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\Moti Begna\\AppData\\Local\\Programs\\Python\\Python37-32\\tcl\\tk8.6"

setup(
    name = "CatRun",
    options = {'build_exe': {'packages': ['pygame']}},
    executables=[
        Executable(
            "CatRun.py",


            )

        ]
    )
