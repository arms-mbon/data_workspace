Here you will find the combination of the quality-controlled (meta)data taken [from PlutoF](https://github.com/arms-mbon/data_workspace/tree/main/qualitycontrolled_data/from_plutof)) and from the [ARMS overview google sheet](https://github.com/arms-mbon/data_workspace/tree/main/qualitycontrolled_data/from_gs).

* [combined_ImageData.csv](https://github.com/arms-mbon/data_workspace/tree/main/qualitycontrolled_data/combined/combined_ImageData.csv): containing the image IDs, filenames and download URLs for each sampling event for each observatory. Where available, the ARMS plate number and face are also indicated (see the [ARMS Handbook](https://github.com/arms-mbon/documentation/tree/main/armsmbon_handbook) for more information). Only the sampling events with images are listed here.  
* [combined_ObservatoryData.csv](https://github.com/arms-mbon/data_workspace/tree/main/qualitycontrolled_data/combined/combined_ObservatoryData.csv): containing the observatory metadata.
* [combined_OmicsData.csv](https://github.com/arms-mbon/data_workspace/tree/main/qualitycontrolled_data/combined/combined_OmicsData.csv): containing the ENA accession numbers for all sequences that have been stored in ENA. Only sampling events for which sequencing has been performed are listed here. NOTE THE REMARKS ON OMICS DATA BELOW.
* [combined_SamplingEventData.csv](https://github.com/arms-mbon/data_workspace/tree/main/qualitycontrolled_data/combined/combined_SamplingEventData.csv): containing a listing of all sampling events that have occurred to date. Included here are incomplete events, where ARMS units have only been deployed and not yet retrieved.

**ATTENTION: Things to consider regarding the omics data in [combined_OmicsData.csv](https://github.com/arms-mbon/data_workspace/tree/main/qualitycontrolled_data/combined/combined_OmicsData.csv)**

***Demultiplexing info***

During the initial phase of the ARMS program, the omics data provided here were generated with two different demultiplexing methods following MiSeq sequencing. Information on this can be found in the * *Gene_XY_demultiplexed* * columns of the [combined_OmicsData.csv](https://github.com/arms-mbon/data_workspace/tree/main/qualitycontrolled_data/combined/combined_OmicsData.csv) file. Where demultiplexing is denoted as “MiSeq (indices)”, sequencing reads were demultiplexed in the standard manner based on the respective sample indices used for library preparation. Reads of these ENA accession numbers still include the respective primer sequences used during marker gene amplification (see MSOP for details on primer sequences). Depending on the downstream analyses applied, those primer sequences may be removed with dedicated tools.
For ENA accession numbers where demultiplexing is denoted as “MiSeq (indices) / cutadapt (primers)”, reads were demultiplexed based on the respective sample indices used for library preparation, as well as the primer sequences used for marker gene amplification. Those reads should already be devoid of the respective primer sequences, but we still recommend a quick check. We urge all users to specifically check the 18S rRNA accessions denoted as “MiSeq (indices) / cutadapt (primers)”, as there are sequencing runs for which the reads still contain primer sequences despite prior trimming. Given the relatively short length of the 18S rRNA amplicons and resulting read-through during sequencing, such reads should be subjected to an additional round of primer-trimming. A simple length filtering prior to downstream analyses should also be performed, as in some rare cases reads with a length of zero bp resulted from the demultiplexing process. Detailed information on the indices used for each sample and for each sequencing run, along with the accession numbers of the original raw files, are provided in the ADD LINK ONCE UPLOADED demultiplexing_details_OmicsData.csv.

***Issues with accessions on ENA***

It can happen that there are problems on [ENA](https://www.ebi.ac.uk/ena/browser/home) with the accessions we have submitted there. This is out of our hands, unfortunately. We here mention these issues and will update this info once problems have been resolved by ENA. As of November 2023, there were issues with the following 18S rRNA accessions:
* [ERR7125542](https://www.ebi.ac.uk/ena/browser/view/ERR7125542): This accession is displayed on ENA with a read and base count of zero and the ENA * *Generated FASTQ Files* * are unavailable. For now, we recommend to download the files desposited under * *Submitted Files* *. These files are good to use.
* ADD INFO ON 18S July 2019 accessions once Sequenced column is in omics data csv

**Quality control**

The metadata here undergo a QC by comparing the PlutoF and google sheet entries as they are combined. Any corrections or additions that are found to be necessary in PlutoF or the google sheet are passed on to the ARMS partners, and once those corrections are made the process is repeated, until no more corrections are necessary. 

_**The current status of the QC**_: :ballot_box_with_check: 

<!---The current status of the QC_: :ballot_box_with_check: :repeat: -->
