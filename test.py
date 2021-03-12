import unthrow
import inspect
import traceback
import sys
import gc
import testmod

fullTrace=[]

class context_blocker:
    def __enter__(self):
        print("Start with")

    def __exit__(self,type,value,traceback):
        print("End with")    


def exceptionTest():
    unthrow.stop("I'm stopping here")

def mainApp(x):
#    import testmod
    unthrow.set_interrupts(50)
    unthrow.traceall=True
    print("RUN IN TEST MODULE")
    testmod.runtest()
    print("RUN IN EXEC")
    exec("for c in range(100):\n  print(c)",{},{})
    print("RUN LOCALLY")
    for c in range(100):
        print(c%10,end=' ')
    print("RUN nothing")
    d=0
#    it=unthrow.test_iter(500)
    it=range(500)
#    while True:
#        d=d+1
    for c in it:
        pass
#    unthrow.traceall=False
#        d=c
#        print(c)
    print("Done nothing",d)
    print("Manual throwing")
    for c in range(10):
        print("L:",c)
        if c==3 or c==5:
            print("TRY THROW")
            exceptionTest()
        print("L2:",c)

    print("RUN BLOCKED by with")
    with context_blocker() as b:
        for c in range(100):
            print(".",end="")
    print("END APP")

resume_info=None
x=["woo"]
while True:
    print("DOING SOMETHING AT TOP LEVEL")
    try:
        if resume_info:
            unthrow.resume(resume_info)
            resume_info=None
        mainApp(x)
        print("DONE")
        break
    except unthrow.ResumableException as e:
        resume_info=e.saved_frames
        #print("Top level:",e.parameter)
print("Doing something outside")
for c in range(100):
    print(".",end="")
resume_info=None
print("RC X3:",sys.getrefcount(x))



