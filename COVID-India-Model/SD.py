import numpy as np

# built in functions
def tabhl( ys,  x,  xl,  xh,  xi):
    # table function to interpolate values
    xs = [i for i in np.arange(xl,xh,xi)]
    for index in range(0, len(xs)):
        if x < xs[index]:
            return ys[index - 1] if index > 0 else ys[index]
    return  ys[len(ys) - 1]
    
def lookup_discrete(x, xs, ys):

    """
    Intermediate values take on the value associated with the next lower x-coordinate (also called a step-wise function). The last two points of a discrete graphical function must have the same y value.
    Out-of-range values are the same as the closest endpoint (i.e, no extrapolation is performed).
    """
    for index in range(0, len(xs)):
        if x < xs[index]:
            return ys[index - 1] if index > 0 else ys[index]

    return ys[len(ys) - 1]



def table(ys,  x,  xl,  xh,  xi):
    xs = [i for i in np.arange(xl,xh,xi)]
    length = len(xs)
    if x < xs[0]:
        dx = xs[1] - xs[0]
        dy = ys[1] - ys[0]
        k = dy / dx
        return ys[0] + (x - xs[0]) * k
    if x > xs[length - 1]:
        dx = xs[length - 1] - xs[length - 2]
        dy = ys[length - 1] - ys[length - 2]
        k = dy / dx
        return ys[length - 1] + (x - xs[length - 1]) * k
    return np.interp(x, xs, ys)

def ttable(xy_tuples, x):
    # alternate version of table with xy tuples
    # table function
    for xs,ys in xy_tuples:
        prev_ys = ys
        if xs == x:
            return ys
        elif xs > x:
            return (prev_ys+ys)/2
        prev_ys = ys

def lookup_extrapolation(x, xs, ys):

    """
    Intermediate values are calculated with linear interpolation between the intermediate points.
    Out-of-range values are calculated with linear extrapolation from the last two values at either end.
    """

    length = len(xs)

    if x < xs[0]:
        dx = xs[1] - xs[0]
        dy = ys[1] - ys[0]
        k = dy / dx
        return ys[0] + (x - xs[0]) * k

    if x > xs[length - 1]:
        dx = xs[length - 1] - xs[length - 2]
        dy = ys[length - 1] - ys[length - 2]
        k = dy / dx
        return ys[length - 1] + (x - xs[length - 1]) * k

    return np.interp(x, xs, ys)
        

def clip(v1,v2,t1,t2):
    return v1 if t1 < t2 else v2
    

def ramp(time, slope, start, finish=0):

    """
    Parameters
    time: The current time of modelling
    slope: float The slope of the ramp starting at zero at time start
    start: float Time at which the ramp begins
    finish: float Optional. Time at which the ramp ends
    Returns
    response: float If prior to ramp start, returns zero If after ramp ends, returns top of ramp

    """
    if time < start:
        return 0
    else:
        if finish <= 0:
            return slope * (time - start)
        elif t > finish:
            return slope * (finish - start)
        else:
            return slope * (time - start)

def step(time, value, tstep):

    """"
    Parameters

    value: float The height of the step
    tstep: float The time at and after which `result` equals `value`
    Returns
    - In range [-inf, tstep) returns 0
    - In range [tstep, +inf] returns `value`
    """
    return value if time >= tstep else 0


def pulse(time, start, duration):

    """ 
    In range [-inf, start) returns 0
    In range [start, start + duration) returns 1
    In range [start + duration, +inf] returns 0
    """
    return 1 if start <= time < start + duration else 0

def ifthenelse(condition, val_if_true, val_if_false):
    if condition:
        return val_if_true
    else:
        return val_if_false

def smooth(self,p,q):
    prev_x = p / q
    smthx = prev_x / q
    r = smthx
    x = prev_x + dt * (p-r)
