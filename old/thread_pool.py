from time import sleep, time
from random import random
from concurrent.futures import ThreadPoolExecutor

# custom task that will sleep for a variable amount of time


def task(name):
    # sleep for less than a second
    sleep(random())
    return name


s_start = time()
for i in range(10):
    print(task(i))

print(f"Single thread time: {time() - s_start}")

t_start = time()
# start the thread pool
with ThreadPoolExecutor(10) as executor:
    # execute tasks concurrently and process results in order
    for result in executor.map(task, range(10)):
        # retrieve the result
        print(result)
print(f"Muliti-thread time taken: {time() - t_start}")
