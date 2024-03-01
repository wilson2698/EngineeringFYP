import pandas as pd
import os

from misc_functions import get_data, get_coefficients, pct_change
from airspeed import get_airspeeds
from blockage_correction import maskell_blockage_correction, correct_blockage
from charts import make_coeff_chart

def ingest_experiment_set(folderpath, output_filepath):
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
    CD_df = correct_blockage(CD_df,br_df, maskell_blockage_correction)

    CL_CD_df = CL_df/CD_df

    ## Calculate Percentage Changes from Clean Config
    CL_change = pct_change(CL_df, "Clean")
    CD_change = pct_change(CD_df, "Clean")
    CL_CD_change = pct_change(CL_CD_df, "Clean")
    
    with pd.ExcelWriter(output_filepath,engine='xlsxwriter') as writer:
        ## Coefficient Values
        CL_df.to_excel(writer, sheet_name="CL",index=True)
        CD_df.to_excel(writer, sheet_name="CD",index=True)
        CL_CD_df.to_excel(writer, sheet_name="CL_CD",index=True)

        workbook = writer.book
        worksheet = workbook._add_sheet('Chart')

        CL_chart = make_coeff_chart("CL", workbook, len(config_list), len(aoas))
        worksheet.insert_chart("A1", CL_chart)
        CD_chart = make_coeff_chart("CD", workbook, len(config_list), len(aoas))
        worksheet.insert_chart("P1", CD_chart)
        CL_CD_chart = make_coeff_chart("CL_CD", workbook, len(config_list), len(aoas))
        worksheet.insert_chart("A40", CL_CD_chart)

        ## Coefficient Change Values
        CL_change.to_excel(writer, sheet_name="CL_change",index=True)
        CD_change.to_excel(writer, sheet_name="CD_change",index=True)
        CL_CD_change.to_excel(writer, sheet_name="CL_CD_change",index=True)

        percent_change_worksheet = workbook._add_sheet('PercentChange')

        CL_change_chart = make_coeff_chart("CL_change", workbook, len(config_list)-1, len(aoas))
        percent_change_worksheet.insert_chart("A1", CL_change_chart)
        CD_change_chart = make_coeff_chart("CD_change", workbook, len(config_list)-1, len(aoas))
        percent_change_worksheet.insert_chart("P1", CD_change_chart)
        CL_CD_change_chart = make_coeff_chart("CL_CD_change", workbook, len(config_list)-1, len(aoas))
        percent_change_worksheet.insert_chart("A40", CL_CD_change_chart)