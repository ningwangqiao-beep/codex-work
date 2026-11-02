"""Wilson event intervals; descriptive only, correlated states need game bootstrap."""
import math

def wilson(positive,total,z=1.96):
    if total<=0:return None
    p=positive/total;den=1+z*z/total;center=(p+z*z/(2*total))/den;half=z*math.sqrt(p*(1-p)/total+z*z/(4*total*total))/den
    return [max(0,center-half),min(1,center+half)]
