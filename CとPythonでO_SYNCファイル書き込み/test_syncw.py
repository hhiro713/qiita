import os
import io
import datetime
import time


TEST_COUNT = 10000
DRIVER_FILE = 'DRIVER'
COMMAND = b'COMMAND'


def test_with_fileio():
    elapsed_time = -1
    with io.FileIO(DRIVER_FILE, mode='w') as file:
        start = time.time()
        for i in range(TEST_COUNT):
            file.seek(0)
            file.write(COMMAND)
            file.flush()
        elapsed_time = (time.time() - start) * 1000000
        file.close()
    print(f'io.FileIO: {elapsed_time / TEST_COUNT:.4f}us')


def test_with_iobase():
    elapsed_time = -1
    with open(DRIVER_FILE, mode='wb', buffering=0) as file:
        start = time.time()
        for i in range(TEST_COUNT):
            file.seek(0)
            file.write(COMMAND)
            file.flush()
        elapsed_time = (time.time() - start) * 1000000
        file.close()
    print(f'io.IOBase: {elapsed_time / TEST_COUNT:.4f}us')


def test_with_os():
    elapsed_time = -1
    fd = os.open(DRIVER_FILE, flags=(os.O_WRONLY | os.O_SYNC))
    start = time.time()
    for i in range(TEST_COUNT):
        os.lseek(fd, 0, os.SEEK_SET)
        os.write(fd, COMMAND)
    os.close(fd)
    elapsed_time = (time.time() - start) * 1000000
    print(f'os: {elapsed_time / TEST_COUNT:.4f}us')


if __name__ == '__main__':
    test_with_fileio()
    test_with_iobase()
    test_with_os()
