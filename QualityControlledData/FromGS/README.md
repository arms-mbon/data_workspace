The data here are taken from the ARMS overview sheet in the ARMS google account: https://docs.google.com/spreadsheets/d/1iFwKO4OAmQrgZtIpyOxjdXvyCEPE_jK45V4elh1lwYs/edit#gid=139664176

*Quality Control*
A QC is done on the google sheet data compared to the data from PlutoF (that are first downloaded and QC'd themself: https://github.com/arms-mbon/Data/tree/main/QualityControlledData/FromPlutoF).
We do the following
* From the ARMS Observatory info tab:the Station names, ARMS unit names, lat,  long, and depth are compared to the same values in the PlutoF download
* If there are differences in lat, long, depth, the PlutoF value is taken, unless not present and the google sheet value is taken. 
* If station or unit names are different they are changed (to be the same in the two data sources) but if lat, long, or depth are not correct we do not change those here
* Rather, these values will be changed in the combined PlutoF and google sheet data, which are in https://github.com/arms-mbon/Data/tree/main/QualityControlledData/Combined

So, to see the original google sheet data, look at the files here:
* GS_ARMS_Material_Samples_and_Sequence_Info.csv
* GS_ARMS_Observatory_Metadata.csv
* GS_ARMS_Observatory_info.csv
* GS_ARMS_Samples_Sequences.csv

To see the QC report (differences, and noting the instructions above for how we responded to those differences) see: 
* qc_report_arms_observatories_plutoF_to_gsheets.csv
* qc_report_arms_observatories_gsheets_to_plutof.csv
