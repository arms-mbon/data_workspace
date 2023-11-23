In here are the input and output files from the first processing batch of PEMA runs on the ARMS-MBON sequences. Bioinformatics processing of the sequencing data from ARMS-MBON's first sampling campaign 2018-2019 (i.e., all ARMS units deployed in 2018 and 2019 and retrieved between 2018 and 2020) was performed in April 2022. 

The following folders are included here:
* [ParameterFiles](https://github.com/arms-mbon/data_workspace/tree/main/analysis_data/from_pema/processing_batch1/parameter_files): the parameter files used as input for the PEMA runs. 
* [The taxonomic assignments](https://github.com/arms-mbon/data_workspace/tree/main/analysis_data/from_pema/processing_batch1/taxonomic_assignments): as output by PEMA, containing ASV/OTU read counts and taxonomy assignments.
* [The fasta files](https://github.com/arms-mbon/data_workspace/tree/main/analysis_data/from_pema/processing_batch1/fasta): as output by PEMA, containing the sequences of each run.

PEMA was run on sequences grouped by marker gene and by MiSeq sequencing run, and each group has its own parameter files, taxonomic assignment files, and fasta files. An overview of the processing -- including the material sample IDs, ENA accession numbers, dates and observatories etc -- from which one can identify which samples were processed in which group, is provided as here. 
* Corrections were necessary to observatory, unit, materialSample, and parameter file names: the overview file to use is therefore [pema_overview_batch1.xlsx](https://github.com/arms-mbon/data_workspace/blob/main/analysis_data/from_pema/processing_batch1/pema_overview_batch1.xlsx)
* The original overview file is provided for provenance reasons: [pema_overview_batch1_old.xlsx](https://github.com/arms-mbon/data_workspace/blob/main/analysis_data/from_pema/processing_batch1/pema_overview_batch1_old.xlsx).
