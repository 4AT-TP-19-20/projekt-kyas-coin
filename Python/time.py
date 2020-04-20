import time

if __name__ == "__main__":
    while True:
        timer = int(time.time())
        if timer == int(time.time()):
            pass
        else:
            timer = int(time.time())
            print(timer % 120)
