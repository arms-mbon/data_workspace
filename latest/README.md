In here are all the data collected from or created by the ARMS programme. 

  * In [qualitycontrolled_data](https://github.com/arms-mbon/Data/tree/main/qualitycontrolled_data) are the data downloaded from various sources and quality checked
  * In [reformatted_data](https://github.com/arms-mbon/Data/tree/main/reformatted_data), these data are combined and reformatted to be published in various endpoints
  * In [analysis_data](https://github.com/arms-mbon/Data/tree/main/analysis_data) are the input and output data from PEMA runs on the ARMS raw sequence data 

Some of these folders are used for harvesting, quality controlling, and formatting: these folders are not interesting for the general user of ARMS-MBON data. Those folders that **are** of interest to the general user are the following:
  * In the [combined data folder](https://github.com/arms-mbon/data_workspace/tree/main/qualitycontrolled_data/combined) are the sampling event, observatory, ENA accession numbers, and image metadata for the ARMS-MBON events to date, after having been quality controlled and combined. A new harvest is done when sufficient new data exist. These are the data that subsequently published, e.g. on EurOBIS etc.
  * In the folder [from pema](https://github.com/arms-mbon/data_workspace/tree/main/analysis_data/from_pema) are selected input and output files from PEMA processing of the ARMS-MBON sequences. Processing is done in separate batches, e.g. [batch 1 can be found here](https://github.com/arms-mbon/data_workspace/tree/main/analysis_data/from_pema/processing_batch1) 
