from gui import gui_main
import asyncio
from qasync import run



# async def main():
#     tasks = [asyncio.create_task(ReceiverFactory.get_games()), asyncio.create_task(gui_main())]
#
#     while len(tasks):
#         done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
#         for task in done:
#             print(task, task.result())

if __name__ == '__main__':
    try:
        run(gui_main())
    except asyncio.exceptions.CancelledError:
        exit(0)
    # loop = asyncio.get_event_loop()
    # try:
    #     loop.run_until_complete(main())
    # finally:
    #     loop.close()