def maskell_blockage_correction(CD_u, br, theta=0.96):
    '''
    This function is ued to find the corrected drag coefficient using Maskell's method
    theta = 0.96 (default) for aerofoils
    theta = 0.9 for blunt shapes
    Cd_u: uncorrected drag coefficient
    br: blockage ratio
    '''
    CD_c = CD_u/(1 + theta*CD_u*br)
    return CD_c

def al_obaidi_blockage_correction(CD_u, br):
    '''
    This function is ued to find the corrected drag coefficient using Maskell's method
    Cd_u: uncorrected drag coefficient
    br: blockage ratio
    '''
    y = 0.005*br**2 + 0.0133*br + 0.022
    CD_c = CD_u*(1-y)
    return CD_c

def correct_blockage(CD_df, br_df, bc_method):
    CD_c_df = CD_df.copy()
    for col in CD_df:
        if col == "AOA":
            continue
        for row in CD_df.index:
            CD_c_df.loc[row,col] = bc_method(CD_df.loc[row,col],br_df.loc[row,col])
    return CD_c_df