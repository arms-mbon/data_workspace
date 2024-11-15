The data here are taken from the ARMS overview sheet in the ARMS google account: https://docs.google.com/spreadsheets/d/1j3yuY5lmoPMo91w6e3kkJ6pmp1X6FVGUtLealuKJ3wE/edit#gid=1607535453. Each tab there is downloaded into a separate CSV file. 

*  [GS_ARMS_Material_Samples_and_Sequence_Info.csv](https://github.com/arms-mbon/data_workspace/blob/main/qualitycontrolled_data/from_gs/GS_ARMS_MaterialSamples_Sequence_Metadata.csv) for the metadata on the sampling events and the accession numbers of the sequences in ENA 
*  [GS_ARMS_Samples_Sequences.csv](https://github.com/arms-mbon/data_workspace/blob/main/qualitycontrolled_data/from_gs/GS_ARMS_MaterialSamples_Sequences.csv) semantic annotation and descriptions of the columns in the samples+sequences spreadsheet 
*  [GS_ARMS_Observatory_info.csv](https://github.com/arms-mbon/data_workspace/blob/main/qualitycontrolled_data/from_gs/GS_ARMS_Observatory.csv) for the metadata on the observatories themselves
*  [GS_ARMS_Observatory_Metadata.csv](https://github.com/arms-mbon/data_workspace/blob/main/qualitycontrolled_data/from_gs/GS_ARMS_Observatory_Metadata.csv) semantic annotation and descriptions of the columns observatories spreadsheet 

**Quality Control**

A QC is done on the google sheet data by comparing them to the data from PlutoF and stored [in from_plutof](https://github.com/arms-mbon/data_workspace/tree/main/qualitycontrolled_data/from_plutof), and by checking for internal consistency. Any differences found are communicated to the ARMS partners who are requested to make corrections in their PlutoF and/or google sheet entries. The data are then downloaded again and the QC steps repeated, until no more corrections are necessary. The QC output files can also be found here (_qc_report_xxx).

_**The status of the QC**_: main checks done; on each harvest a comparison to the [plutof](https://github.com/arms-mbon/data_workspace/tree/main/qualitycontrolled_data/from_plutof) data are done and differences corrected

