The data here are taken from the ARMS overview sheet in the ARMS google account: https://docs.google.com/spreadsheets/d/1iFwKO4OAmQrgZtIpyOxjdXvyCEPE_jK45V4elh1lwYs/edit#gid=139664176

**Quality Control**

A QC is done on the google sheet data by comparing them to the data from PlutoF and stored [in FromPlutoF here](https://github.com/arms-mbon/Data/tree/main/QualityControlledData/FromPlutoF). 
We do the following
* From the ARMS Observatory info tab: the Station names, ARMS unit names, lat, long, and depth are compared to the same values in the PlutoF download
  * If station or unit names are different, they are changed to be the value that was agreed in the consortium (both google sheet and PlutoF may need to be changed). 
  * If lat, long, or depth are not different, we assume that the PlutoF value is to be trusted (unless otherwise informed), and if there is no value then "not provided" is entered instead. A copy of the google sheet downloaded tabs is created, with a additional columns containing the corrected lat, long, and depth values. 
* From the ARMS samples+sequences tab: TO BE WRITTEN!!!!!!!

So, to see the original google sheet data, look at the files here:
*  [GS_ARMS_Material_Samples_and_Sequence_Info.csv](https://raw.githubusercontent.com/arms-mbon/Data/edit/main/QualityControlledData/FromGS/GS_ARMS_Material_Samples_and_Sequence_Info.csv)
*  [GS_ARMS_Observatory_Metadata.csv](https://raw.githubusercontent.com/arms-mbon/Data/edit/main/QualityControlledData/FromGS/GS_ARMS_Observatory_Metadata.csv)
*  [GS_ARMS_Observatory_info.csv](https://raw.githubusercontent.com/arms-mbon/Data/edit/main/QualityControlledData/FromGS/GS_ARMS_Observatory_info.csv)
*  [GS_ARMS_Samples_Sequences.csv](https://raw.githubusercontent.com/arms-mbon/Data/edit/main/QualityControlledData/FromGS/GS_ARMS_Samples_Sequences.csv)

The corrected google sheet values can be found 
* [GS_ARMS_Material_Samples_and_Sequence_Info_QC.csv](https://raw.githubusercontent.com/arms-mbon/Data/edit/main/QualityControlledData/FromGS/GS_ARMS_Material_Samples_and_Sequence_Info_QC.csv)
* [GS_ARMS_Observatory_Metadata_QC.csv](https://raw.githubusercontent.com/arms-mbon/Data/edit/main/QualityControlledData/FromGS/GS_ARMS_Observatory_Metadata_QC.csv)
* [GS_ARMS_Observatory_info_QC.csv](https://raw.githubusercontent.com/arms-mbon/Data/edit/main/QualityControlledData/FromGS/GS_ARMS_Observatory_info_QC.csv)
* [GS_ARMS_Samples_Sequences_QC.csv](https://raw.githubusercontent.com/arms-mbon/Data/edit/main/QualityControlledData/FromGS/GS_ARMS_Samples_Sequences_QC.csv)

To see the QC report see: 
* [From PlutoF to Google Sheet](https://raw.githubusercontent.com/arms-mbon/Data/edit/main/QualityControlledData/FromGS/qc_report_arms_observatories_plutoF_to_gsheets.csv)
* [From Google Sheet to PlutoF](https://raw.githubusercontent.com/arms-mbon/Data/edit/main/QualityControlledData/FromGS/qc_report_arms_observatories_gsheets_to_plutof.csv)
* for the samples sheets here also ....!!!!!!

