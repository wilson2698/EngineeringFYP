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