In here are all the metadata that are downloaded on a regular basis from the ARMS-MBON account on PlutoF.

The organisation of folders is by Observatory. In each Observatory folder are spreadsheets (CSV) that contain the metadata provided in PluotF by the ARMS partners
* An _overview_ of the sampling events that are recorded in PlutoF, including the metadata of the observatory, ARMS units, and events, and also including the number of material samples, associated data, sequences, and observations that are in PlutoF for each event.
* A listing of the _associated data_ for each sampling event, this including the plate images and spreadsheets with visual observations. File names and download links are given here. 
* Listings of the metadata that are associated with the following PlutoF entry types: _material samples_, _observations_, _sequences_. Note that as our primary use of PlutoF is to store the event metadata and plate images, these spreadsheets will probably be incomplete
  * a fuller listing of the _material samples_ can be found in the [FromGS](https://github.com/arms-mbon/Data/tree/main/QualityControlledData/FromGS) and [Combined](https://github.com/arms-mbon/Data/tree/main/QualityControlledData/Combined) folders
  * the _observation_ data (detected species) is incomplete as we are not currently using PlutoF as the prime location for storing this information; any visual observation files created during the sampling events will be list as _associated data_, and additional observations will be published via biodiversity archives (TBC)
  * the _sequences_ refer to ASVs, and is also incomplete as we are not currently using PlutoF as the prime location for storing this information; raw sequences are stored in ENA and the accession numbers can be found in the [FromGS](https://github.com/arms-mbon/Data/tree/main/QualityControlledData/FromGS) and [Combined](https://github.com/arms-mbon/Data/tree/main/QualityControlledData/Combined) folders, and species determinations made therefrom will be published via biodiversity archives (TBC)

In addition to these spreadsheets contained in each observatory folder, the same information are contained in these all-observatory spreadsheets
* [AllOverview.csv](https://github.com/arms-mbon/Data/blob/main/QualityControlledData/FromPlutoF/AllOverview.csv)
* [AllAssociatedData.csv](https://github.com/arms-mbon/Data/blob/main/QualityControlledData/FromPlutoF/AllAssociatedData.csv)
* [AllMaterialSamples.csv](https://github.com/arms-mbon/Data/blob/main/QualityControlledData/FromPlutoF/AllMaterialSamples.csv)
* [AllSequences.csv](https://github.com/arms-mbon/Data/blob/main/QualityControlledData/FromPlutoF/AllSequences.csv)
* [AllObservations.csv](https://github.com/arms-mbon/Data/blob/main/QualityControlledData/FromPlutoF/AllObservations.csv)

The metadata downloaded from PlutoF undergo a QC, which modifies the various names (observatory, ARMS units) and IDs (event IDs, material sample IDs, sequence IDs, associated data IDs) where they do follow the rules encoded in the ARMS-MBON Handbook. The QC script and its inputs and outputs can also be found here.

