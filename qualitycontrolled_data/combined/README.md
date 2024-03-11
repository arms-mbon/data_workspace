## ARMS-MBON combined and quality-controlled (meta)data

Here you will find the combination of the quality-controlled (meta)data taken [from PlutoF](https://github.com/arms-mbon/data_workspace/tree/main/qualitycontrolled_data/from_plutof)) and from the [ARMS overview google sheet](https://github.com/arms-mbon/data_workspace/tree/main/qualitycontrolled_data/from_gs).

* [combined_ImageData.csv](https://github.com/arms-mbon/data_workspace/tree/main/qualitycontrolled_data/combined/combined_ImageData.csv): containing the image IDs, filenames and download URLs for the images each observatory uploaded for their sampling events. Where available, the ARMS plate number and face are also indicated (see the [ARMS Handbook](https://github.com/arms-mbon/documentation/tree/main/armsmbon_handbook) for more information). Only the sampling events that have images are listed here.  
* [combined_ObservatoryData.csv](https://github.com/arms-mbon/data_workspace/tree/main/qualitycontrolled_data/combined/combined_ObservatoryData.csv): containing the observatory metadata.
* [combined_OmicsData.csv](https://github.com/arms-mbon/data_workspace/tree/main/qualitycontrolled_data/combined/combined_OmicsData.csv): containing the ENA accession numbers for all sequences that have been stored in ENA. Only sampling events for which sequencing has been performed are listed here. NOTE THE REMARKS ON OMICS DATA BELOW.
* [combined_SamplingEventData.csv](https://github.com/arms-mbon/data_workspace/tree/main/qualitycontrolled_data/combined/combined_SamplingEventData.csv): containing a listing of all sampling events that have occurred to date. Included here are incomplete events, where ARMS units have only been deployed and not yet retrieved. NOTE THE REMARKS ON SAMPLING EVENT DATA BELOW.
*  [combined_OtherDataFiles.csv](https://github.com/arms-mbon/data_workspace/tree/main/qualitycontrolled_data/combined/combined_OtherDataFiles.csv): containing the IDs, filenames and download URLs for other files that the observatories uploaded for their sampling events, e.g. spreadsheets containing information about the images or visual observations.
*  For each data file there is a metadata file that explains what the columns are and what type of values are contained therein.

Three additional files which are not the combination of previous data 
*  [demultiplexing_details_OmicsData.csv](https://github.com/arms-mbon/data_workspace/blob/main/qualitycontrolled_data/combined/ENA-accession-numbers.xlsx), which is explained below.
*  [ENA-accession-numbers.xlsx](https://github.com/arms-mbon/data_workspace/blob/main/qualitycontrolled_data/combined/ENA-accession-numbers.xlsx) which is a list of all the sample (SAMEA) and run (ERR) accession numbers for the ARMS-MBON data in ENA, for each project (PRJEB), of which there is a separate project for each country. All projects are linked under the ARMS-MBON project [PRJEB72316](https://www.ebi.ac.uk/ena/browser/view/prjeb72316). The sample ID (as added to ENA, which is often somewhat different from the material sample IDs as otherwise recorded here) are also provided, along with the sequencing run (run 1 or run 2) number (see the next bullet point to understand this).
*  [A list of field/area and sample/technical replicates](https://github.com/arms-mbon/data_workspace/blob/main/qualitycontrolled_data/combined/ReplicatesList.csv) with the materialSampleID followed by the replicate IDs. Field/Area replicates are used when ARMS units are about about 10m or less apart (in the 3 dimensions) and are deployed and retrieved within a few days of each other. These ARMS units have different names (e.g. VH1 and VH2). Sample/technical replicates were used for some material samples with poor results from the first run on the sequencing, and so new sequencing was done on stored material. For these we have changed the material sample ID to append a "_r1" (replicate 1 used for run 1) or "_r2" (replicate 2 used for run 2), and the replicate ID is then the material sample ID without this appendix. Note that in the combined files here we have not changed the material sample IDs in this same way, rather we have added a column to indicate if a sequence accession number is the result of "sequencing run 1 or 2". These "run 1/2" information have also been added to the file [ENA-accession-numbers.xlsx](https://github.com/arms-mbon/data_workspace/blob/main/qualitycontrolled_data/combined/ENA-accession-numbers.xlsx). The only differnce between these sample/technical replicates are that they produced difference sequences, everthing before that stage is the same. 

**Quality control**

The metadata here undergo a QC by comparing the PlutoF and google sheet entries as they are combined. Any corrections or additions that are found to be necessary in PlutoF or the google sheet are passed on to the ARMS partners, and once those corrections are made the process is repeated, until no more corrections are necessary. 

_**The current status of the QC**_: :ballot_box_with_check: 

<!---The current status of the QC_: :ballot_box_with_check: :repeat: -->

### ATTENTION: Things to consider regarding the omics data in [combined_OmicsData.csv](https://github.com/arms-mbon/data_workspace/tree/main/qualitycontrolled_data/combined/combined_OmicsData.csv)

***Demultiplexing info***

During the initial phase of the ARMS programme, the omics data accessible from ENA were generated with two different demultiplexing methods following MiSeq sequencing. Information on which method was followed can be found in the *Gene_XY_demultiplexed* columns of the [combined_OmicsData.csv](https://github.com/arms-mbon/data_workspace/tree/main/qualitycontrolled_data/combined/combined_OmicsData.csv) file. 
* Where demultiplexing is denoted as “MiSeq (indices)”, sequencing reads were demultiplexed in the standard manner based on the respective sample indices used for library preparation. Reads of these ENA accession numbers still include the respective primer sequences used during marker gene amplification (see MSOP for details on primer sequences). Depending on the downstream analyses applied, those primer sequences may be removed with dedicated tools.
* For ENA accession numbers where demultiplexing is denoted as “MiSeq (indices) / cutadapt (primers)”, reads were demultiplexed based on the respective sample indices used for library preparation, as well as the primer sequences used for marker gene amplification. Those reads should already be devoid of the respective primer sequences, but we still recommend a quick check.

*We urge all users to specifically check the 18S rRNA accessions denoted as “MiSeq (indices) / cutadapt (primers)”*, as there are sequencing runs for which the reads still contain primer sequences despite prior trimming. Given the relatively short length of the 18S rRNA amplicons and resulting read-through during sequencing, such reads should be subjected to an additional round of primer-trimming. A simple length filtering prior to downstream analyses should also be performed, as in some rare cases reads with a length of zero bp resulted from the demultiplexing process. Detailed information on the indices used for each sample and for each sequencing run, along with the accession numbers of the original raw files, are provided in the [demultiplexing_details_OmicsData.csv](https://github.com/arms-mbon/data_workspace/blob/main/qualitycontrolled_data/combined/demultiplexing_details_OmicsData.csv) file.

***Issues with accessions on ENA***

It can happen that there are problems on [ENA](https://www.ebi.ac.uk/ena/browser/home) with the accessions we have submitted there. This is, unfortunately, out of our hands. We here mention these issues we are aware of, and will update this info once problems have been resolved by ENA. As of February 2024, there were issues with the following 18S rRNA accessions:
* [ERR7125542](https://www.ebi.ac.uk/ena/browser/view/ERR7125542): This accession is displayed on ENA with a read and base count of zero and the ENA *Generated FASTQ Files* are unavailable. For now, we recommend to download the files desposited under *Submitted Files*. These files are good to use.
* ADD INFO ON 18S July 2019 accessions once Sequenced column is in omics data csv

### Remarks on the sampling event data in [combined_SamplingEventData.csv](https://github.com/arms-mbon/data_workspace/blob/main/qualitycontrolled_data/combined/combined_SamplingEventData.csv)

***Preservative info***

For events from 2018 and 2019, both ETOH and DMSO could be used (see the [ARMS Handbook](https://github.com/arms-mbon/documentation/tree/main/armsmbon_handbook) for details). Note that the preservative could be DMSO or DMSO-EDTA-NaCl, i.e. DESS, this distinction was not tracked for these early sampling events. Later on, only DESS has been used. 
