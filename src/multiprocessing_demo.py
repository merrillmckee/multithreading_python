import math
import time

import concurrent.futures


def cpu_bound_simulator(task_num):
    """
    Simulates a CPU bound task that takes task_num seconds to complete

    Parameters
    ----------
    task_num:
        Both task number and number of seconds this task will take

    Returns
    -------
        Returns task_num + 100
    """

    start = time.time()

    values = list(range(100))
    while True:
        if time.time() - start > task_num:
            # stop looping when time limit hit
            break
        x = time.time()
        i = int(x * 100) % 100
        values[i] = math.sqrt(x) * math.sqrt(1 + x)

    if task_num == 2:
        # Simulate an exception
        raise NotImplementedError("Some type of error in CPU bound call")
    return 100 + task_num


def get_task_list(n_tasks):
    # task list in reverse order: [8, 7, 6, ..., 3, 2, 1]
    task_list = list(range(1, n_tasks + 1))[::-1]
    return task_list


def singleprocess_demo():
    """
    Demonstrates the default single process version of the multiprocessing_demo below as a reference.
    """
    print("Single process\n")

    task_list = get_task_list(n_tasks=8)

    start = time.time()
    for task_num in task_list:
        try:
            result = cpu_bound_simulator(task_num)
            print(f"Completed task {result} in {time.time() - start:.3f} seconds")
        except Exception as e:
            print(f"cpu_bound_simulator raised an exception: {e}")


def multiprocessing_demo():
    """
    Demonstrates Python multiprocessing by running 8 CPU bound (simulated) tasks in parallel.
    """
    print("Multiprocessing\n")

    n_workers = 8
    task_list = get_task_list(n_tasks=8)

    with concurrent.futures.ProcessPoolExecutor(max_workers=n_workers) as executor:

        futures = [executor.submit(cpu_bound_simulator, task_num) for task_num in task_list]

        start = time.time()
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                print(f"Completed task {result} in {time.time() - start:.3f} seconds")
            except Exception as e:
                print(f"cpu_bound_simulator raised an exception: {e}")


if __name__ == "__main__":

    singleprocess_demo()
    multiprocessing_demo()

    # Example console output
    #
    # Single process
    #
    # Completed task 108 in 8.000 seconds
    # Completed task 107 in 15.000 seconds
    # Completed task 106 in 21.000 seconds
    # Completed task 105 in 26.000 seconds
    # Completed task 104 in 30.000 seconds
    # Completed task 103 in 33.000 seconds
    # cpu_bound_simulator raised an exception: Some type of error in CPU bound call
    # Completed task 101 in 36.000 seconds
    # Multiprocessing
    #
    # Completed task 101 in 1.096 seconds
    # cpu_bound_simulator raised an exception: Some type of error in CPU bound call
    # Completed task 103 in 3.094 seconds
    # Completed task 104 in 4.094 seconds
    # Completed task 105 in 5.093 seconds
    # Completed task 106 in 6.093 seconds
    # Completed task 107 in 7.093 seconds
    # Completed task 108 in 8.093 seconds
