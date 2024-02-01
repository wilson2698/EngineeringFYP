import pandas as pd
import os
from math import sin, radians

def get_data(filepath):
    '''
    This function serves to get the mean readings from the *.csv file output from the FT sensor.
    Output is a pandas series
    '''
    df = pd.read_csv(filepath)
    output = df[["Force X (N)","Force Y (N)", "Force Z (N)", "Torque X (N-m)", "Torque Y (N-m)", "Torque Z (N-m)"]].mean()
    return output

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

def get_coefficients(data, V):
    '''
    This function serves to calculate the CL and CD of the airfoil from the lift and drag forces from get_data()
    '''
    rho_air = 1.18 #kg/m^3
    S = 32940.88019/(1000**2) #m^2 From solidworks
    lift = data["Force X (N)"]
    drag = data["Force Y (N)"]

    ## 2L/(rho*V^2*S)
    half_rho_v2_s = 0.5*rho_air*(V**2)*S
    CL = lift/half_rho_v2_s
    CD = drag/half_rho_v2_s ## Not Blockage Corrected Yet
    return [CL, CD]

def ingest_experiment_set(folderpath):
    '''
    Ingest and calculate for each aoa in each configuration in each experiment set
    '''
    ## Intialise aoa for referencing and storage
    aoas = [-15, -10, -5, 0, 5, 10, 15]
    ## Initialise filenames
    aoa_dict = {
        -15:"neg15deg.csv", 
        -10:"neg10deg.csv",
        -5:"neg5deg.csv",
        0:"0deg.csv",
        5:"pos5deg.csv",
        10:"pos10deg.csv",
        15:"pos15deg.csv"
        }
    config_list = os.listdir(folderpath)
    config_list = list(filter(lambda x: os.path.isdir(f"{folderpath}/{x}"), config_list))

    ## Initialise Outputs
    CL_df = pd.DataFrame({"AOA":aoas})
    CD_df = pd.DataFrame({"AOA":aoas})
    CL_CD_df = pd.DataFrame({"AOA":aoas})
    ## For each configuration
    for config in config_list:
        ## Get airspeeds from file
        airspeeds = get_airspeeds(folderpath,config)
        config_CL_temp = []
        config_CD_temp = []
        config_CL_CD_temp = []

        ## For each angle of attack
        for aoa in aoas:
            filepath = f"{folderpath}/{config}/{aoa_dict[aoa]}"
            temp = get_data(filepath)
            CL,CD = get_coefficients(temp, airspeeds[aoa])
            config_CL_temp += [CL]
            config_CD_temp += [CD]
            config_CL_CD_temp += [CL/CD]
        CL_df.loc[:, config] = config_CL_temp
        CD_df.loc[:,config] = config_CD_temp
        CL_CD_df.loc[:,config] = config_CL_CD_temp
    
    with pd.ExcelWriter("Data/FT1/output.xlsx",engine='xlsxwriter') as writer:
        CL_df.to_excel(writer, sheet_name="CL",index=False)
        CD_df.to_excel(writer, sheet_name="CD",index=False)
        CL_CD_df.to_excel(writer, sheet_name="CL_CD",index=False)

        workbook = writer.book
        worksheet = workbook._add_sheet('Chart')

        CL_chart = make_coeff_chart("CL", workbook, len(config_list), len(aoas))
        worksheet.insert_chart("A1", CL_chart)
        CD_chart = make_coeff_chart("CD", workbook, len(config_list), len(aoas))
        worksheet.insert_chart("P1", CD_chart)
        CL_CD_chart = make_coeff_chart("CL_CD", workbook, len(config_list), len(aoas))
        worksheet.insert_chart("A40", CL_CD_chart)

    
def make_coeff_chart(coeff_name, workbook, n_configs, n_aoas):
    '''
    coeff_name is the sheet name which has the coefficient data (will aslo be used to name the chart and axis)
    n_configs is the number of configurations
    n_aoas is the number of angle of attacks recorded
    '''
    chart = workbook.add_chart({'type':'scatter', "subtype": "straight_with_markers"})
    ## Iterate through all configurations
    for i in range(n_configs):
        col = i + 1 # Skip AOA Column
        chart.add_series({
            'name': [coeff_name,0,col],
            'categories': [coeff_name, 1, 0, n_aoas, 0],
            'values': [coeff_name, 1, col, n_aoas, col],
        })
    chart.set_x_axis({
        'name': 'AOA',
        'major_gridlines': {
            'visible':True,
            'line': {'width':0.75, 'dash_type':'solid'}
        }
        })
    chart.set_y_axis({
        'name': coeff_name,
        'major_gridlines': {
            'visible':True,
            'line': {'width':0.75, 'dash_type':'solid'}
        }
        })
    chart.set_legend({'position': 'bottom'})
    chart.set_title({'name': f'{coeff_name} agaisnt AOA'})
    chart.set_size({'x_scale': 1.7, 'y_scale': 2.5})


    return chart
    


ingest_experiment_set("Data/FT1")