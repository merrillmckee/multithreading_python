import asyncio
import time

from work_simulators import io_bound_simulator, io_bound_simulator_async


def get_task_list(n_tasks):
    # task list in reverse order: [8, 7, 6, ..., 3, 2, 1]
    task_list = list(range(1, n_tasks + 1))[::-1]
    return task_list


def singlethreaded_demo():
    """
    Demonstrates the default single threaded version of the async_demo below as a reference.
    """
    print("\nSingle threaded; no concurrency\n")

    task_list = get_task_list(n_tasks=8)

    start = time.time()
    for task_num in task_list:
        try:
            result = io_bound_simulator(task_num)
            print(f"Completed task {result} in {time.time() - start:.3f} seconds")
        except Exception as e:
            print(f"io_bound_simulator raised an exception: {e}")


async def async_demo():
    """
    Demonstrates Python async IO by running 8 IO bound (simulated) tasks concurrently.
    """
    print("\nConcurrency with AsyncIO\n")

    task_list = get_task_list(n_tasks=8)
    tasks = [io_bound_simulator_async(task_num) for task_num in task_list]

    start = time.time()
    for task in asyncio.as_completed(tasks):
        try:
            result = await task
            print(f"Completed task {result} in {time.time() - start:.3f} seconds")
        except Exception as e:
            print(f"io_bound_simulator raised an exception: {e}")


if __name__ == "__main__":

    singlethreaded_demo()
    asyncio.run(async_demo())

    # Example console output
    #
    # Single threaded; no concurrency
    #
    # Completed task 108 in 8.002 seconds
    # Completed task 107 in 15.007 seconds
    # Completed task 106 in 21.010 seconds
    # Completed task 105 in 26.016 seconds
    # Completed task 104 in 30.021 seconds
    # Completed task 103 in 33.026 seconds
    # io_bound_simulator raised an exception: Some type of error in IO bound call
    # Completed task 101 in 36.034 seconds
    #
    # Concurrency with AsyncIO
    #
    # Completed task 101 in 1.002 seconds
    # io_bound_simulator raised an exception: Some type of error in async IO bound call
    # Completed task 103 in 3.002 seconds
    # Completed task 104 in 4.001 seconds
    # Completed task 105 in 5.002 seconds
    # Completed task 106 in 6.001 seconds
    # Completed task 107 in 7.001 seconds
    # Completed task 108 in 8.002 seconds
    #
    # Process finished with exit code 0
