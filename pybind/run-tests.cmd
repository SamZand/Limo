@ECHO OFF

:: Allow lemonator.pyb to be imported
SET PYTHONPATH = "$(pwd)\build"
pytest tests/test.py