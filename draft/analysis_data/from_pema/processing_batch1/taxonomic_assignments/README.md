Here are the output files containing the taxonomic assignments from the PEMA processing of the ARMS-MBON sequences. 

The first chunk of files are "Extended final tables" that contain the following information:
* an ASV/OTU identifier (these numbers being unique with a single PEMA run)
* the number of reads for each sample that was processed: each sample is in a separate column, with the title being the material sample ID that can be found in ENA (note: these material sample IDs are not always exactly the same as used in the sampling logsheets in the [sample data folder](https://github.com/arms-mbon/data_workspace/tree/main/qualitycontrolled_data/combined), but they are close)  
* the full taxonomic classification as returned by the reference database used
* the associated NBCI taxon ID (where there is one)
   
Their filenames contain:
* the date the samples were sequenced (e.g. April2021)
* the gene type (COI, ITS, 18S)
* whether or not the blank (sequences) were included

The second chunk of files are the more detailed taxonomic assignements, containing:
* an ASV/OTU identifier  (these numbers being unique with a single PEMA run; the first part of this ID, before the "_", is included in the ID in the first column of its linked Extended_final_table)
* For each node of the taxonomic classification: its name and its confidence level
  
Their filenames contain:
* the date the samples were sequenced (e.g. April2021)
* the gene type (COI, ITS, 18S)

There is also a file indicating which samples produced [no results](https://github.com/arms-mbon/data_workspace/blob/main/analysis_data/from_pema/processing_batch1/taxonomic_assignments/Samples_with_no_results.xlsx). 
