from unthrow import *
import ray
ray.init()

@ray.remote
def work(t):
    from time import sleep
    print("BEFORE SLEEP")
    sleep(t)
    print("SLEEP DONE")
    return t

def step(t):
    print("start work")
    o = work.remote(t)
    print("prep to stop")
    print("stop", stop(o))

    print("resumed")
    print(">>>>> ray.get()", ray.get(o))
    return ray.get(o)



def p(f, *args, **kwargs):
    f(*args, **kwargs)

p(id, 1)

r = Resumer()
r.run_once(step, 2)
import pickle
print('dumps')
x = pickle.dumps(r)
print("x=", x)
print("now wait")
print(r.resume_params)
ray.wait([r.resume_params])
print(ray.get(r.resume_params))

def is_working(x):
    rr = pickle.loads(x)
    assert rr.finished is False
    print("rr=", rr)
    print('>>loaded')
    print(">>finally", rr.run_once(step, 2))
is_working(x)
