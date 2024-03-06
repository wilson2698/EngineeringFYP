import os

from Ingestor import ingest_experiment_set, average_CL_CD
from charts import make_excel

## Directory to find experiment folders from and where to save outputs
data_dir = "Data"
output_dir = "Outputs"

## Make output directory if not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

## Find only folders from directory
dir_list = os.listdir(data_dir)
exp_folders = list(filter(lambda x: os.path.isdir(f"{data_dir}/{x}"), dir_list))


### Uncomment and Run these to ingest data and get output graphs accordingly

## Sample for testing
# output = ingest_experiment_set(f"{data_dir}/Sample", output_filepath=f'Outputs/Sample.xlsx', blockage_correction_method="raw")

bc_methods = ['raw','maskell','al_obaidi']

for bc_method in bc_methods:
    if not os.path.exists(f'{output_dir}/{bc_method}'):
        os.makedirs(f'{output_dir}/{bc_method}')

    CL_list = []
    CD_list = []
    for exp in exp_folders:
        if exp == "Sample": # Ignore sample data
            continue
        temp_output = ingest_experiment_set(
            f"{data_dir}/{exp}", 
            output_filepath=f'{output_dir}/{bc_method}/{exp}_results.xlsx', 
            blockage_correction_method=bc_method
            )
        CL_list += [temp_output[0]]
        CD_list += [temp_output[1]]

    CL_avg, CD_avg = average_CL_CD(CL_list, CD_list)
    output = make_excel(CL_avg, CD_avg, f'{output_dir}/{bc_method}/averaged_results.xlsx')