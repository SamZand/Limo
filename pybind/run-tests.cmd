@ECHO OFF

:: Allow lemonator.pyb to be imported
set PYTHONPATH=%cd%\build
pytest tests/test.py
