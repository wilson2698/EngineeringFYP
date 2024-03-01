import os

from Ingestor import ingest_experiment_set

## Directory to find experiment folders from
data_dir = "Data"

## Make output directory if not exist
if not os.path.exists("Outputs"):
    os.makedirs("Outputs")

## Find only folders from directory
dir_list = os.listdir(data_dir)
exp_folders = list(filter(lambda x: os.path.isdir(f"{data_dir}/{x}"), dir_list))


### Uncomment and Run these to ingest data and get output graphs accordingly

## Sample for testing
# ingest_experiment_set(f"{data_dir}/Sample", output_filepath=f'Outputs/Sample.xlsx', blockage_correction_method="raw")

for exp in exp_folders:
    if exp == "Sample": 
        continue
    ingest_experiment_set(
        f"{data_dir}/{exp}", 
        output_filepath=f'Outputs/{exp}_maskell.xlsx', 
        blockage_correction_method="Maskell"
        )