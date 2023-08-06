# pydiary
MatLab style commands logger for the Python interpreter

## Usage
The package exports a single class.
```python
from pydiary import Diary

Diary()                 # Turns diary on, saving commands to the default file diary.py
Diary('mydiary.py')     # Turns diary on, saving commands to a file called mydiary.py in the current directory
my_diary = Diary()      # You can save a reference to the Diary instance to use it later

...

# The current active diary is automatically assigned to a variable called "diary"
diary.off()             # Turns diary off

my_diary.on()           # Turns on the previously created diary
```
