import time
import multiprocessing

def sleep_for_a_bit(seconds):
    print(f"sleepint {seconds} seconds(s)")
    time.sleep(seconds)
    print("done sleeping")


# p1=multiprocessing.Process(target=sleep_for_a_bit,args=[1])
# p2=multiprocessing.Process(target=sleep_for_a_bit,args=[1])

process=[]

for p in range(3):
    p=multiprocessing.Process(target=sleep_for_a_bit,args=[1])
    if __name__=="__main__":
        p.start()
        

    # p2.start()
    # p3.start()
    # p1.join()
    # p2.join()
    # p3.join()


finish=time.perf_counter()

print("finished runnign after sec: ",finish)