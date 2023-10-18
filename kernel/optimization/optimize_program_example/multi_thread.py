import threading
import time

rounds = 4
max_num = 100_000_000


def summing():
    start = 0
    end = start + max_num
    ret = 0

    for i in range(end) :
        ret += 1
    
    print("ret : ", ret)

if __name__ == "__main__":
    print("Multi Thread")

    start = time.perf_counter()

    threads = []
    for i in range(rounds):
        task = threading.Thread(target=summing, args=())
        task.start()
        threads.append(task)

    for thread in threads:
        thread.join()

    finish = time.perf_counter()

    print(f'Finished in {round(finish-start, 2)} second(s)')
    print()