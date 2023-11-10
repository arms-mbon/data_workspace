The source data from the ARMS-MBON project are harvested and placed here. These data are subjected to a basic quality control. The steps followed are  
  * Metadata and data are downloaded from PlutoF to [from_plutof](https://github.com/arms-mbon/Data/tree/main/qualitycontrolled_data/from_plutof), this being the project data management platform used by ARMS-MBON
  * Metadata are extracted from the ARMS-MBON overview google sheet to [from_gs](https://github.com/arms-mbon/Data/tree/main/qualitycontrolled_data/from_gs)
  * Both sources of data are corrected where values are clearly wrong (date formatting, ID malformations, etc).
  * The GS and PlutoF data are then combined, based on the materialSample IDs. These combined data are in [combined](https://github.com/arms-mbon/Data/tree/main/qualitycontrolled_data/combined): this includes the observatory, event, sample, omics, and image data. **These are the data that are of interest to the general user**

_**The status of the QC**_: main checks have been made, however with each harvest new checks are run and minor corrections made



