Here are the output files containing read count tables and taxonomic assignments from the PEMA processing of the ARMS-MBON sequence data. 

The __Extended_final_table__ files contain the following information:
* an ASV/OTU identifier of the following format:
  * For COI: __ASV_XY:ID__. The ID part matches the ID in the corresponding __tax_assignments__ and __fasta__ files. The "ASV" part of the identifier is unique _within_ a single PEMA run, while the "ID" part is unique for each DNA sequence and can therefore occur in files across processing runs. This means that while ASV_1 for example can occur in each sequencing run
  * For 18S: __OtuXY__. The identifiers are unique _within_ a single PEMA run
* the number of reads for each sample that was processed: each sample is in a separate column, with the title being the material sample ID that can be found in ENA  
* the full taxonomic classification as returned by the reference database used
* the taxon name and the NBCI taxon ID for the taxon level within that full classification for which an ID could be found 

Important Information for PEMA v.2.1.4 Users: 
In this version of PEMA, for COI gene sequences, the taxonomic classification in these tables stops at the genus level. The species-level classification is not included in the Extended Final Tables. To obtain species-level classification for COI gene sequences, users should refer to the "tax_assignments" files (see below). These documents include detailed classifications beyond the genus level for each ASV provided in the Extended Final Tables.
   
The filenames of the extended final tables contain:
* the date the samples were sequenced (e.g. April2021)
* the gene type (COI, ITS, 18S)
* whether or not the blank (sequences) were included

The second chunk of files are the more detailed "taxonomic assignements", containing:
* an ASV/OTU identifier (these numbers being unique with a single PEMA run; the first part of this ID, before the "_", is included in the ID in the first column of its associated Extended_final_table)
* For each level in the taxonomic classification: its name and its confidence level
  
Their filenames contain:
* the date the samples were sequenced (e.g. April2021)
* the gene type (COI, ITS, 18S)

There is also a file indicating which samples produced [no results](https://github.com/arms-mbon/data_workspace/blob/main/analysis_data/from_pema/processing_batch1/taxonomic_assignments/Samples_with_no_results.xlsx) and those which [were removed because they occurred in the blanks](https://github.com/arms-mbon/data_workspace/blob/main/analysis_data/from_pema/processing_batch1/taxonomic_assignments/OTUs_ASVs%20that%20were%20removed_modified%20because%20they%20occurred%20in%20the%20blanks.xlsx)

Note: the sample IDs as used by PEMA were not all correctly aligned with the Material Sample IDs used in the rest of the ARMS dataset, however these were corrected manually in the files that you see here. 
