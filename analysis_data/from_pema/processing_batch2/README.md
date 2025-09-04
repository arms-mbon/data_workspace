In here are the input and output files from the second processing batch of PEMA runs on the ARMS-MBON sequences, which was the first one that used the LifeWatch IJI workflow. This covers the bioinformatics processing of the sequencing data from ARMS-MBON's sampling campaign 2020-2021 (i.e., all ARMS units deployed and retrieved between 2020 and 2021), where the processing was performed in chunks between September 2020 and August 2023.

The folders and files that are the outputs of processing_batch2 can be found in [analysis_release_002](https://github.com/arms-mbon/analysis_release_002/tree/main): all the files of processing_batch2 contributed to data_release_002. 


The following folders are included:
* [Parameter files](https://github.com/arms-mbon/analysis_release_002/tree/main/parameter_files): the parameter files used as input for the PEMA runs. 
* [The taxonomic assignments](https://github.com/arms-mbon/analysis_release_002/tree/main/taxonomic_assignments): as output by PEMA, containing ASV/OTU read count tables (corrected for ASVs/OTUs occuring in blank samples), ASV/OTU taxonomy assignments and files denoting which ASVs/OTUs got removed/modified because they occurred in blank samples, and a file indicating which samples did not yield any ASVs/OTUs.
* [Curated taxonomic assignments for 18S and COI](https://github.com/arms-mbon/analysis_release_002/tree/main/taxonomic_assignments): files named _TaxonomyCurated and _TaxonomyFull are PEMA taxonomic classification outputs for 18S and COI that have been curated. For 18S, so that we could make a more correct assignment of taxonomic names to those from WoRMS (World Register of Marine Species), for COI to correct a bug in the version of PEMA used.  
* [The fasta files](https://github.com/arms-mbon/analysis_release_002/tree/main/fasta): as output by PEMA, containing the sequences of each run.

PEMA was run on sequences grouped by marker gene and by MiSeq sequencing run, and each group has its own parameter files, taxonomic assignment files, and fasta files. An overview of the processing - including the material sample IDs, ENA accession numbers, dates and observatories etc - from which one can identify which samples were processed in which group, can be found in 
[pema_overview_batch2.xlsx](https://github.com/arms-mbon/analysis_release_002/blob/main/pema_overview_batch2.xlsx).
