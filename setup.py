from cx_Freeze import setup, Executable

base = None    

executables = [Executable("vaccine-check.py", base=base)]

packages = ["idna", "requests", "tkinter", "time", "dateutil", "datetime"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "VaccineCheck",
    options = options,
    version = "1.0",
    description = 'Check vaccines for centers in Ballarpur',
    executables = executables
)