import os

from Ingestor import ingest_experiment_set

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
# ingest_experiment_set(f"{data_dir}/Sample", output_filepath=f'Outputs/Sample.xlsx', blockage_correction_method="raw")

bc_method = "raw" # ['raw','maskell']

for exp in exp_folders:
    if exp == "Sample": # Ignore sample data
        continue
    ingest_experiment_set(
        f"{data_dir}/{exp}", 
        output_filepath=f'{output_dir}/{exp}_{bc_method}.xlsx', 
        blockage_correction_method=bc_method
        )
