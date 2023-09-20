"""
SD points are the points of the standard curve.
"""

import numpy as np
import scipy.optimize as optimization

def is_more_than_4_sd_points(sd_points:list) -> bool:
    """
    sd_points: [[x1, y1], [x2, y2], ...]

    We need at least 4 points to fit the standard curve. (The minimum points taken by mycurvefit.com is 4.)

    return True if the number of sd_points is more than 4
    """
    if len(sd_points) >= 4:
        return True
    else:
        return False

def arrange_sd_points_in_order(sd_points:list) -> list:
    """
    sd_points: [[x1, y1], [x2, y2], ...]

    x is the concentration of the standard solution
    y is the signal intensity of the standard solution
    sort sd_points by x1, x2, x3, ...

    return [[x1, y1], [x2, y2], ...]
    """
    sd_points = sorted(sd_points, key=lambda x: x[0])

    return sd_points

def determin_sd_slope(sd_points:list) -> str:
    """
    sd_points: [[x1, y1], [x2, y2], ...]
    
    return the slope of the standard curve ("pos" or "neg")
    """
    sd_points = arrange_sd_points_in_order(sd_points)
    d_signal = sd_points[-1][1] - sd_points[0][1]
    d_conc = sd_points[-1][0] - sd_points[0][0]
    if d_signal * d_conc > 0:
        return "pos"
    elif d_signal * d_conc < 0:
        return "neg"
    else:
        raise ValueError("The slope of the standard curve is zero.")

def cal_init_paras(sd_points:list) -> list:
    """
    sd_points: [[x1, y1], [x2, y2], ...]

    The first step of fitting is to calculate the initial parameters.

    init_A: bottom signal intensity
    init_B: 1 or -1 accroding to the slope
    init_C: mid-point concentration
    init_D: top signal intensity

    return [ini_A, ini_B, ini_C, ini_D]
    """
    sd_points = arrange_sd_points_in_order(sd_points)
    xs = [x[0] for x in sd_points]
    ys = [y[1] for y in sd_points]
    sd_slope = determin_sd_slope(sd_points)

    init_A = min(ys)*0.9 # bottom signal intensity
    if sd_slope == "pos":
        init_B = 1                
    elif sd_slope == "neg":
        init_B = -1
    init_C = np.median(xs) # mid-point concentration
    init_D = max(ys)*1.1 # top signal intensity

    return [init_A, init_B, init_C, init_D]

def cal_fitting_paras(sd_points:list, init_paras:list, maxfev=50000) -> list:
    """
    sd_points: [[x1, y1], [x2, y2], ...]
    init_paras: [ini_A, ini_B, ini_C, ini_D]
    maxfev: the maximum number of iterations

    Use scipy.optimize.curve_fit to fit the standard curve.
    
    return [A, B, C, D]
    """
    xs = [x[0] for x in sd_points]
    ys = [y[1] for y in sd_points]
    sigma = ys # this is for weight = 1/(y^2)

    params, params_covariance = optimization.curve_fit(fourPL, xs, ys, 
                                                            p0=init_paras, 
                                                            sigma=sigma, 
                                                            absolute_sigma=True, 
                                                            maxfev=maxfev)
        
    return params


######
# Fitting function
######

def fourPL(x, A, B, C, D) -> float:
    """
    x is the concentration of the standard solution
    we use the four parameters after fitting to find the signal intensity.
    A: bottom
    B: slope
    C: mid-point
    D: top

    return the signal intensity of the standard solution (y)
    """
    return ((A-D)/(1.0+(np.sign((x/C)) * (np.abs((x/C)))**(B))) + D)

def find_the_conc(y, A, B, C, D) -> float:
    """
    y is the measured signal
    we use the four parameters after fitting to find the conc. by rearranging the equation. 
    A: bottom
    B: slope
    C: mid-point
    D: top

    return the concentration of the standard solution (x)
    """
    return C * (((A-D)/(y-D)-1)**(1/B))






