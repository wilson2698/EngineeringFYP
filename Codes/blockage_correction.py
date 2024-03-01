import pandas as pd

def maskell_blockage_correction(Cd_u, br, theta=0.96):
    '''
    This function is ued to find the corrected drag coefficient using Maskell's method
    theta = 0.96 (default) for aerofoils
    theta = 0.9 for blunt shapes
    Cd_u: uncorrected drag coefficient
    br: blockage ratio
    '''
    Cd_c = Cd_u/(1 + theta*Cd_u*br)
    return Cd_c

def correct_blockage(CD_df, br_df, bc_method):
    CD_c_df = CD_df.copy()
    for col in CD_df:
        if col == "AOA":
            continue
        for row in CD_df.index:
            CD_c_df.loc[row,col] = bc_method(CD_df.loc[row,col],br_df.loc[row,col])
    return CD_c_df