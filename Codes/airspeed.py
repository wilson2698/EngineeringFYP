import pandas as pd 

from math import sin, radians

def airspeed_from_pitot(h_static, h_total):
    ## Constants
    rho_h20 = 1000 #kg/m^3
    g = 9.81 #m/s^2
    rho_air = 1.18 #kg/m^3
    theta = 30 #Angle of manometer in degrees

    dynamic_pressure = ((h_total-h_static)/1000)*sin(radians(theta))*rho_h20*g
    U_inf = (dynamic_pressure/(0.5*rho_air))**0.5

    return U_inf

def get_airspeeds(folder,config):
    airspeeds = {}
    h_readings = pd.read_excel(f"{folder}/AirSpeedTracker.xlsx", sheet_name=config, index_col="AOA")
    
    for aoa in h_readings.index:
        airspeeds[aoa] = airspeed_from_pitot(h_readings.loc[aoa,"Hstatic"], h_readings.loc[aoa,"Htotal"])
    
    return airspeeds