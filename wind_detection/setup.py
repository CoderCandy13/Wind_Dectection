from cx_Freeze import setup, Executable

setup(
    name="WindInfoApp",
    version="1.0",
    description="Your Wind Information App",
    executables=[Executable("wind.py", base="Win32GUI")],
)
