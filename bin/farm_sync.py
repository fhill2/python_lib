#!/usr/bin/env -S ${HOME}/.venv/python_lib/bin/python
import sys
print(sys.executable)

if __name__ == '__main__':
    from starfarm.farm import Farm
    farm = Farm()
    farm.sync()
