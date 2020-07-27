import cx_Freeze

executables = [cx_Freeze.Executable("BallPit.py")]

cx_Freeze.setup(
    name="BallPit",
    options={"build_exe":{"packages":["pygame"],"include_files":["assets\GameOver700.png","assets\logo32.png","assets\Menu700.png","assets\Paused700.png"]}},
    description = "Welcome to the Ball Pit",
    executables = executables
    )
