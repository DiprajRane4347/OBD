from cx_Freeze import setup,Executable

setup(name="Object Detection Software",
      version="0.1",
      description= "This Software Detects Objects in realtime enviornment",
      executables=[Executable("main.py")]
      )
