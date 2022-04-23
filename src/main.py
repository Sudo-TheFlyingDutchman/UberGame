from gui import gui_main
import asyncio
from qasync import run


if __name__ == '__main__':
    try:
        run(gui_main())
    except asyncio.exceptions.CancelledError:
        exit(0)