import multiprocessing
import time


def task():
    x = 1
    while True:
        print(x)
        x += 1


p1 = multiprocessing.Process(target=task)


def called():
    global p1
    p1.start()
    time.sleep(5)
    stopper()


def stopper():
    global p1
    p1.terminate()


if __name__ == "__main__":
    called()
