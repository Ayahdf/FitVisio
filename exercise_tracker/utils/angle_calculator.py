import math

def calculate_angle(a, b, c):
    """Calculates the angle between three points in degrees"""
    a = (a[0], a[1])
    b = (b[0], b[1])
    c = (c[0], c[1])
    
    # Get vectors
    ba = (a[0]-b[0], a[1]-b[1])
    bc = (c[0]-b[0], c[1]-b[1])
    
    # Calculate dot product and magnitudes
    dot_product = ba[0] * bc[0] + ba[1] * bc[1]
    magnitude_ba = math.sqrt(ba[0]**2 + ba[1]**2)
    magnitude_bc = math.sqrt(bc[0]**2 + bc[1]**2)
    
    # Calculate angle in radians then convert to degrees
    angle = math.acos(dot_product / (magnitude_ba * magnitude_bc))
    return math.degrees(angle)