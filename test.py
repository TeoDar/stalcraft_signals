import multiprocessing as mp
from time import sleep


def f():
    s = 20
    while s > 0:
        sleep(1)
        print(s,'\r')
        s-=1



def main():
    proc = mp.Process(target=f)
    proc.start()
    sleep(3)
    proc.terminate()
    


if __name__=='__main__':
    main()
