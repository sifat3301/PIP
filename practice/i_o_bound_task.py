import threading
import time

"""
Total time ~2 seconds, not 8 second.
"""

def io_task():
    time.sleep(2)  # simulate network call
    print("Done")

threads = []
start = time.time()
for i in range(4):  # 4 threads
    t = threading.Thread(target=io_task)
    t.start()
    threads.append(t)

for t in threads:
    t.join()
end = time.time()
print("Time taken:", end - start)
