[PEMA](https://github.com/hariszaf/pema) is the metabarcoding analysis pipeline we use to process the COI, 18S, and ITS raw sequences obtained from the ARMS-MBON samples. The raw sequences are deposted in [ENA](https://www.ebi.ac.uk/ena/browser/home). 

PEMA runs were executed in batches, with the first batch being for the first ARMS-MBON sampling campaign (i.e., the majority of samples collected from 2018 to 2020). Within each processing batch, the data are further grouped by marker gene and by MiSeq sequencing run, resulting in multiple of PEMA runs per batch. 

The parameters of each PEMA run are input via a parameter file: these parameter files, the output tables including taxonomic assignments, and the output fasta files can be found in the batch folders. Currently we have 
  * [the first batch](https://github.com/arms-mbon/data_workspace/tree/main/analysis_data/from_pema/processing_batch1) covering samples from ARMS-MBON's frist sampling campaign 2018-2020. 

These PEMA outputs are the source data for the species identifications published in EurOBIS, which can also be found here in 
  * [data_release_001](https://github.com/arms-mbon/data_release_001) (the EurOBIS DwC files and the sampling event files) and [analysis_release_001](https://github.com/arms-mbon/analysis_release_001) (the specific PEMA files related to the this data release)
  
