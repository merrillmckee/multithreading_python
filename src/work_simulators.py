import asyncio
import math
import time


def io_bound_simulator(task_num):
    """
    Simulates an IO bound task that takes task_num seconds to complete

    Parameters
    ----------
    task_num:
        Both task number and number of seconds this task will take

    Returns
    -------
        Returns task_num + 100
    """

    time.sleep(task_num)
    if task_num == 2:
        # Simulate an IO exception
        raise NotImplementedError("Some type of error in IO bound call")
    return 100 + task_num


async def io_bound_simulator_async(task_num):
    """
    Simulates an async IO bound task that takes task_num seconds to complete

    Parameters
    ----------
    task_num:
        Both task number and number of seconds this task will take

    Returns
    -------
        Returns task_num + 100
    """
    await asyncio.sleep(task_num)
    if task_num == 2:
        # Simulate an IO exception
        raise NotImplementedError("Some type of error in async IO bound call")
    return 100 + task_num


def cpu_bound_simulator(task_num):
    """
    Simulates a CPU bound task that takes roughly task_num seconds to complete on my macbook

    Parameters
    ----------
    task_num:
        Both task number and number of seconds this task will take

    Returns
    -------
        Returns task_num + 100
    """

    total_iterations = 3_800_000 * task_num

    values = list(range(100))
    n = 0
    while n < total_iterations:
        x = time.time()  # random-ish number
        i = int(x * 100) % 100  # random-ish index to store the result

        # calculation with a couple "slow" square roots
        values[i] = math.sqrt(x) * math.sqrt(1 + x)

        # counter
        n += 1

    if task_num == 2:
        # Simulate an exception
        raise NotImplementedError("Some type of error in CPU bound call")
    return 100 + task_num
