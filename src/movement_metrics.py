"""
Movement metric calculations for GPS telemetry data.
Computes step distance, bearing, speed, and turning angle between 
consecutive GPS fixes for tracked animals.
"""

import numpy as np
from math import radians, degrees, sin, cos, atan2, sqrt


def haversine_m(lat1, lon1, lat2, lon2):
    """
    Straight-line (great-circle) distance in meters between two lat/lon points.
    """
    R = 6371000
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi/2)**2 + cos(phi1)*cos(phi2)*sin(dlambda/2)**2
    return 2*R*atan2(sqrt(a), sqrt(1-a))


def bearing_deg(lat1, lon1, lat2, lon2):
    """
    Compass bearing in degrees (0-360) from point 1 to point 2.
    """
    phi1, phi2 = radians(lat1), radians(lat2)
    dlambda = radians(lon2 - lon1)
    x = sin(dlambda) * cos(phi2)
    y = cos(phi1)*sin(phi2) - sin(phi1)*cos(phi2)*cos(dlambda)
    return (degrees(atan2(x, y)) + 360) % 360


def add_movement_metrics(group):
    """
    Given one animal's GPS fixes (sorted by time), compute step distance,
    time elapsed, bearing, speed, and turning angle between consecutive fixes.
    Expects columns: 'location-lat', 'location-long', 'timestamp'.
    """
    group = group.copy()
    lat = group['location-lat'].values
    lon = group['location-long'].values
    t = group['timestamp'].values

    dist_m = [np.nan]
    dt_s = [np.nan]
    bearing = [np.nan]

    for i in range(1, len(group)):
        d = haversine_m(lat[i-1], lon[i-1], lat[i], lon[i])
        dt = (t[i] - t[i-1]) / np.timedelta64(1, 's')
        b = bearing_deg(lat[i-1], lon[i-1], lat[i], lon[i])
        dist_m.append(d)
        dt_s.append(dt)
        bearing.append(b)

    group['step_dist_m'] = dist_m
    group['step_dt_s'] = dt_s
    group['bearing_deg'] = bearing
    group['speed_mps'] = group['step_dist_m'] / group['step_dt_s']

    group['turn_angle_deg'] = group['bearing_deg'].diff()
    group['turn_angle_deg'] = (group['turn_angle_deg'] + 180) % 360 - 180

    return group
