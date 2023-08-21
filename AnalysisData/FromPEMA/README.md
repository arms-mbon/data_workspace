[PEMA](https://github.com/hariszaf/pema) is a bioinformatics code we use to process the COI, 18S, and ITS raw sequences obtained from the ARMS-MBON samples. 

The sequences processed are in [ENA](https://www.ebi.ac.uk/ena/browser/home). PEMA runs were executed in batches, and within each batch we processed the sequences in chunks (based mainly on gene type, but sometimes on other considerations). The parameters of each run are input via a parameter file: these parameter files, the output taxonomic assignments, and the output fasta files can be found in the batch folders. Currently we have 
* [the first batch](https://github.com/arms-mbon/data_workspace/tree/main/AnalysisData/FromPEMA/processing_batch001) covering samples collected from 2018 to 2020

  
