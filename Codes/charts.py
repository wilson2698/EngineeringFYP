import pandas as pd

from misc_functions import pct_change

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
    chart.set_title({'name': f'{coeff_name} against AOA'})
    chart.set_size({'x_scale': 1.7, 'y_scale': 2.5})


    return chart


def make_excel(CL_df, CD_df, output_filepath):
    CL_CD_df = CL_df/CD_df

    ## Calculate Percentage Changes from Clean Config
    CL_change = pct_change(CL_df, "Clean")
    CD_change = pct_change(CD_df, "Clean")
    CL_CD_change = pct_change(CL_CD_df, "Clean")

    n_aoas, n_config = CL_df.shape

    with pd.ExcelWriter(output_filepath,engine='xlsxwriter') as writer:
        ## Coefficient Values
        CL_df.to_excel(writer, sheet_name="CL",index=True)
        CD_df.to_excel(writer, sheet_name="CD",index=True)
        CL_CD_df.to_excel(writer, sheet_name="CL_CD",index=True)

        workbook = writer.book
        worksheet = workbook._add_sheet('Chart')

        CL_chart = make_coeff_chart("CL", workbook, n_config, n_aoas)
        worksheet.insert_chart("A1", CL_chart)
        CD_chart = make_coeff_chart("CD", workbook, n_config, n_aoas)
        worksheet.insert_chart("P1", CD_chart)
        CL_CD_chart = make_coeff_chart("CL_CD", workbook, n_config, n_aoas)
        worksheet.insert_chart("A40", CL_CD_chart)

        ## Coefficient Change Values
        CL_change.to_excel(writer, sheet_name="CL_change",index=True)
        CD_change.to_excel(writer, sheet_name="CD_change",index=True)
        CL_CD_change.to_excel(writer, sheet_name="CL_CD_change",index=True)

        percent_change_worksheet = workbook._add_sheet('PercentChange')

        CL_change_chart = make_coeff_chart("CL_change", workbook, n_config-1, n_aoas)
        percent_change_worksheet.insert_chart("A1", CL_change_chart)
        CD_change_chart = make_coeff_chart("CD_change", workbook, n_config-1, n_aoas)
        percent_change_worksheet.insert_chart("P1", CD_change_chart)
        CL_CD_change_chart = make_coeff_chart("CL_CD_change", workbook, n_config-1, n_aoas)
        percent_change_worksheet.insert_chart("A40", CL_CD_change_chart)

        return [CL_df, CD_df, CL_CD_df,CL_change, CD_change, CL_CD_change]