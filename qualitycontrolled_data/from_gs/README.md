The data here are taken from the ARMS overview sheet in the ARMS google account: https://docs.google.com/spreadsheets/d/1j3yuY5lmoPMo91w6e3kkJ6pmp1X6FVGUtLealuKJ3wE/edit#gid=1607535453. Each tab there is downloaded into a separate CSV file. 

*  [GS_ARMS_Material_Samples_and_Sequence_Info.csv](https://raw.githubusercontent.com/arms-mbon/Data/main/QualityControlledData/FromGS/GS_ARMS_Material_Samples_and_Sequence_Info.csv) for the metadata on the sampling events and the accession numbers of the sequences in ENA 
*  [GS_ARMS_Samples_Sequences.csv](https://raw.githubusercontent.com/arms-mbon/Data/main/QualityControlledData/FromGS/GS_ARMS_Samples_Sequences.csv) semantic annotation and descriptions of the columns in the samples+sequences spreadsheet 
*  [GS_ARMS_Observatory_info.csv](https://raw.githubusercontent.com/arms-mbon/Data/main/QualityControlledData/FromGS/GS_ARMS_Observatory_info.csv) for the metadata on the observatories themselves
*  [GS_ARMS_Observatory_Metadata.csv](https://raw.githubusercontent.com/arms-mbon/Data/main/QualityControlledData/FromGS/GS_ARMS_Observatory_Metadata.csv) semantic annotation and descriptions of the columns observatories spreadsheet 

**Quality Control**

A QC is done on the google sheet data by comparing them to the data from PlutoF and stored [in FromPlutoF](https://github.com/arms-mbon/Data/tree/main/QualityControlledData/FromPlutoF), and by checking for internal consistency. Any differences found are communicated to the ARMS partners who are requested to make corrections in their PlutoF and/or google sheet entries. The data are then downloaded again and the QC steps repeated, until no more corrections are necessary. The QC output files can also be found here (_qc_report_xxx).

_**The current status of the QC**_: :repeat:

<!---The current status of the QC_: :ballot_box_with_check: -->

