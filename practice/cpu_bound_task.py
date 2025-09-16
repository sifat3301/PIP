import threading
import time
"""
Here I use 4 thread where almost take same time as 1thread.
"""

def cpu_task():
    count = 0
    for i in range(10_000_000):
        count += i
    print(count)

threads = []
start = time.time()
for i in range(4):  # 4 threads
    t = threading.Thread(target=cpu_task)
    t.start()
    threads.append(t)

for t in threads:
    t.join()
end = time.time()
print("Time taken:", end - start)


