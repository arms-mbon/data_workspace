Here are the output files containing read count tables and taxonomic assignments from the PEMA processing of the ARMS-MBON sequence data. 

The __Extended_final_table__ files contain the following information:

* ASV/OTU identifiers of the following format:
  * For COI: __ASV_XY:ID__. The ID part matches the ID in the corresponding __tax_assignments__ and __fasta__ files. The "ASV" part of the identifier is unique _within_ a single PEMA run, while the "ID" part is unique for each DNA sequence and can therefore occur in files across processing runs. This means that while the "ASV_1" prefix for example can occur in each sequencing run, it does not necessarily represent the same DNA sequence in these runs, while the ID is unqiue across all runs for each unique sequence.
  * For 18S and ITS: __OtuXY__. The identifiers match the identifiers in the corresponding __fasta__ files for each run and they are unique _within_ a single PEMA run. This means that while "Otu 1" for example can occur in each sequencing run, it does not necessarily represent the same DNA sequence across runs. Unique sequences across runs can be identified by matching OTUs/ASVs to the seqeuences in the fasta files. Because there was an error within PEMA at the time of usage regarding the sequence identifier format for ITS runs, the sequence identifiers in these files are of the format OtuXY. However, these sequences represent ASVs clustered with Swarm v2.

* The read counts for each ASV/OTU in each sample that was processed, i.e., columns up to the third last column represent material sample IDs. 
  
* The second last column contains the full taxonomic classification as returned by the respective reference database in a single character string. __NOTE:__ In PEMA v2.1.4 used here, taxonomy of COI sequences is denoted only to genus level in these tables. The species-level classification is not included in these tables. To obtain species-level classification for COI gene sequences, users should refer to the __tax_assignments__ files (see below). 
  
* The last column contains the NBCI taxon ID and taxon name for the lowest taxonomic level the respective ASV/OTU could be assigned to and for which and NCBI taxon ID could be found. 

* The filenames contain:
  * The date the samples were sequenced (e.g., April2021)
  * The marker gene (i.e., COI, ITS, 18S)
  * The __noBlank__ denotion: This means that a) negative control samples were already removed; b) potential contaminant sequences (OTUs/ASVs that were more abundant in the negative control samples compared to actual samples) were removed; and c) for OTUs/ASVs that were present in negative control samples in lower abundances than in actual samples, their corresponding read number in the negative controls was subtracted from their read number in actual samples.

The __tax_assignements__ files are only generated for COI data and contain:

* ASV identifiers of the format __ID_readAbundance__. The ID part matches the ID part in the corresponding Extended_final_table file (see above).
  
* For each level in the taxonomic classification: its assignment and correspoding confidence value as determined by the RDP classifier used for COI classification.
  
* These documents include detailed classifications beyond the genus level for each ASV provided in the Extended Final Tables.
  
* The filenames contain:
  * The date the samples were sequenced (e.g., April2021)
  * The marker gene (only COI in this case)
  * The __noBlank__ dentotion, which means potential contaminant ASVs that were more abundant in the negative control samples compared to actual samples were removed.

We also provide files indicating which samples produced [no ASVs/OTUs](https://github.com/arms-mbon/data_workspace/blob/main/analysis_data/from_pema/processing_batch1/taxonomic_assignments/Samples_with_no_results.xlsx) and which [ASVs/OTUs were removed or whose counts were adjusted because they occurred in the blanks](https://github.com/arms-mbon/data_workspace/blob/main/analysis_data/from_pema/processing_batch1/taxonomic_assignments/OTUs_ASVs%20that%20were%20removed_modified%20because%20they%20occurred%20in%20the%20blanks.xlsx).
