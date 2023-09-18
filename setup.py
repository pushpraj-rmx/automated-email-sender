import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["email", "smtplib", "email.mime.multipart", "email.mime.text", "random"],
    "excludes": [],
    "include_files": [],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # For a GUI application on Windows

executables = [
    Executable("gui.py", base=base, targetName="windows-email.exe")
]

setup(
    name="YourApp",
    version="1.0",
    description="Your Email Sender App",
    options={"build_exe": build_exe_options},
    executables=executables
)
