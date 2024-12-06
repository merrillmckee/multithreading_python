import time

from concurrent.futures import as_completed, ThreadPoolExecutor


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


def get_task_list(n_tasks):
    # task list in reverse order: [8, 7, 6, ..., 3, 2, 1]
    task_list = list(range(1, n_tasks + 1))[::-1]
    return task_list


def singlethreaded_demo():
    """
    Demonstrates the default single threaded version of the multithreading_demo below as a reference.
    """
    print("Single threaded\n")

    task_list = get_task_list(n_tasks=8)

    start = time.time()
    for task_num in task_list:
        try:
            result = io_bound_simulator(task_num)
            print(f"Completed task {result} in {time.time() - start:.3f} seconds")
        except Exception as e:
            print(f"io_bound_sleep_three raised an exception: {e}")


def multithreading_demo():
    """
    Demonstrates Python multithreading by running 8 IO bound (simulated) tasks in parallel.
    """
    print("Multi-threaded\n")

    n_workers = 8
    task_list = get_task_list(n_tasks=8)


    with ThreadPoolExecutor(max_workers=n_workers) as executor:

        futures = [executor.submit(io_bound_simulator, task_num) for task_num in task_list]

        start = time.time()
        for future in as_completed(futures):
            try:
                result = future.result()
                print(f"Completed task {result} in {time.time() - start:.3f} seconds")
            except Exception as e:
                print(f"io_bound_sleep_three raised an exception: {e}")


if __name__ == "__main__":

    singlethreaded_demo()
    multithreading_demo()

    # Example console output
    #
    # Single threaded
    #
    # Completed task 108 in 8.005 seconds
    # Completed task 107 in 15.009 seconds
    # Completed task 106 in 21.011 seconds
    # Completed task 105 in 26.013 seconds
    # Completed task 104 in 30.019 seconds
    # Completed task 103 in 33.020 seconds
    # io_bound_sleep_three raised an exception: Some type of error in IO bound call
    # Completed task 101 in 36.026 seconds
    #
    #
    # Multi-threaded
    #
    # Completed task 101 in 1.004 seconds
    # io_bound_sleep_three raised an exception: Some type of error in IO bound call
    # Completed task 103 in 3.000 seconds
    # Completed task 104 in 4.005 seconds
    # Completed task 105 in 5.002 seconds
    # Completed task 106 in 6.003 seconds
    # Completed task 107 in 7.003 seconds
    # Completed task 108 in 8.003 seconds
