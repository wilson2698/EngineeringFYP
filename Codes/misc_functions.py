import pandas as pd

def get_data(filepath):
    '''
    This function serves to get the mean readings from the *.csv file output from the FT sensor.
    Output is a pandas series
    '''
    df = pd.read_csv(filepath)
    output = df[["Force X (N)","Force Y (N)", "Force Z (N)", "Torque X (N-m)", "Torque Y (N-m)", "Torque Z (N-m)"]].mean()
    return output

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

def pct_change(df, base_col):
    '''
    Function here calculates the difference between the value and base value,
    a negative sign shows a decrease while a positive sign is an increase
    '''
    out = pd.DataFrame()
    out.index = df.index
    for col in df:
        if col == base_col:
            continue
        temp = ((df[col] - df[base_col])/abs(df[base_col]))*100
        out[col] = temp
    return out

def pct_change2(df):
    compare_dict = {
        "Clean":["1b","3b","5b","7b","9b"],
        "1b": ["1b_3b","1b_5b","1b_7b","1b_9b"],
        "3b": ["1b_3b","3b_5b","3b_7b","3b_9b"],
        "5b": ["1b_5b","3b_5b","5b_7b","5b_9b"],
        "7b": ["1b_7b","3b_7b","5b_7b","7b_9b"],
        "9b": ["1b_9b","3b_9b","5b_9b","7b_9b"],
    }
    out = pd.DataFrame()
    out.index = df.index
    for base_col in compare_dict:
        for col in compare_dict[base_col]:
            temp = ((df[col] - df[base_col])/abs(df[base_col]))*100
            out[col] = temp
    return out