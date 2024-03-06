import pandas as pd
import os

from misc_functions import get_data, get_coefficients
from airspeed import get_airspeeds
from blockage_correction import maskell_blockage_correction, correct_blockage, al_obaidi_blockage_correction
from charts import make_excel

def ingest_experiment_set(folderpath, output_filepath=False, blockage_correction_method="raw"):
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

    ## For each configuration
    for config in config_list:
        ## Get airspeeds from file
        airspeeds = get_airspeeds(folderpath,config)
        config_CL_temp = []
        config_CD_temp = []

        ## For each angle of attack
        for aoa in aoas:
            filepath = f"{folderpath}/{config}/{aoa_dict[aoa]}"
            temp = get_data(filepath)
            CL,CD = get_coefficients(temp, airspeeds[aoa])
            config_CL_temp += [CL]
            config_CD_temp += [CD]

        CL_df.loc[:, config] = config_CL_temp
        CD_df.loc[:,config] = config_CD_temp

    ## Set AOA as index
    CL_df = CL_df.set_index("AOA")
    CD_df = CD_df.set_index("AOA")

    ## get blockage ratios
    br_df = pd.read_excel("Data/Frontal Area.xlsx", sheet_name="Blockage_Ratio")
    br_df = br_df.set_index("AOA")

    ## Find corrected drag coefficient based on blockage ratio
    if blockage_correction_method.lower() =="raw":
        print("Using uncorrected CD")
    elif blockage_correction_method.lower() == "maskell":
        print("Using Maskell's Blockage Correction Method")
        CD_df = correct_blockage(CD_df,br_df, maskell_blockage_correction)
    elif blockage_correction_method== "al_obaidi":
        print("Using Al-Obaidi's Blockage Correction Method")
        CD_df = correct_blockage(CD_df,br_df, al_obaidi_blockage_correction)
    else:
        print("Unknown blockage correction, using uncorrected CD instead")

    if output_filepath:
        return make_excel(CL_df, CD_df, output_filepath)
    else:
        return [CL_df, CD_df]
    
def average_CL_CD(CL_list, CD_list):
    CL_temp = pd.concat(CL_list)
    CD_temp = pd.concat(CD_list)

    CL_avg = CL_temp.groupby(CL_temp.index).mean()
    CD_avg = CD_temp.groupby(CD_temp.index).mean()

    return CL_avg, CD_avg