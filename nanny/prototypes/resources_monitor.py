import time
import psutil

if __name__ == "__main__":
    while True:
        print(f"CPU: {psutil.cpu_percent()}%, memory usage {psutil.virtual_memory().percent}%")
        time.sleep(10)
