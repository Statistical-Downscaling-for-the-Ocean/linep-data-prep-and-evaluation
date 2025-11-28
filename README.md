
# data-prep-and-evaluation
This repository contains:
- The `validate-linep` cli source code for teams to validate their data _before_ submission
- Argo data prep
- Water properties data prep
- Workflows for data statistics, preprocessing, model evaluation and post-processing

## The `validate-linep` cli tool
We provide a CLI tool for validating LineP pressure-profile datasets (netcdf files) against predefined metadata schemas.
Supports multiple dataset types (`CTD`, `BGC`, `STRETCH`) with built-in YAML configs.

### Installation
We strongly recommend using a fresh virtual environment for this tool.

```bash
# recommended installing with uv
uv install git+https://github.com/Statistical-Downscaling-for-the-Ocean/linep-data-prep-and-evaluation.git
```

Or using bare pip
```bash
git clone https://github.com/Statistical-Downscaling-for-the-Ocean/linep-data-prep-and-evaluation.git
cd linep-validator
pip install .
```

This will install the script which can be accessed with `validate-linep`

### Basic usage

to check the expected schema run

```bash
validate-linep schema
# for bgc or stretch submissions run
validate-linep --dataset-type bgc schema
# or
validate-linep --dataset-type stretch schema
```

to validate your submission file, run

```bash
validate-linep validate /path/to/dataset.nc
# or for bgc
validate-linep --dataset-type bgc validate /path/to/dataset.nc
# or for stretch
validate-linep --dataset-type stretch validate /path/to/dataset.nc
```

The `validate` command does the following:

1. Check that dimensions match the schema.
2. Check that required variables exist.
3. Check that coordinates are present and correctly shaped.
4. Warn if units do not match expectations (case-insensitive).


## waterproperties_data_prep
- LineP_save_annual_dataframe.ipynb - Notebook to subset the raw data downloaded from waterproperties.ca
outputs: https://hpfx.collab.science.gc.ca/dfo/SD-Ocean/observations_LineP/OSD_Archive/raw_extract/
- Bin_LineP_raw.ipynb - Notebook to bin data into 1m pressure bins. 
 outputs: https://hpfx.collab.science.gc.ca/dfo/SD-Ocean/observations_LineP/OSD_Archive/binned/
