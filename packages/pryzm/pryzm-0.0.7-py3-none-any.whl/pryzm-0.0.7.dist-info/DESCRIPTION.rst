## Pryzm, color convenient class for linux/mac cli

### Install it


```pip install pryzm```

### Use it
```
from pryzm import *
pr = Pryzm()
print pr.fg('Red Text') # prints in red foreground
print pr.encode([31,47], "Red font with white background")
```

### Change log
* 0.4 Add screen_size
* 0.3 Add some cursor movement
* 0.2 Add encode convenience function
* 0.1 Initial commit, fg_ bg_ at_ functions


