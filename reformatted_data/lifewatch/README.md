Here we have placed all the data that the LifeWatch Tesseracto ARMS workflow requires. These data are provided for a specific purpose and with a specific layout, and while the data here are openly accessible, this is not the place to look for the overview of the ARMS data if you are coming to this page with that intent. 

* [ARMS4Tesseract_data.csv](https://raw.githubusercontent.com/arms-mbon/Data/main/LifeWatch/ARMS4Tesseract_data.csv): the CSV file containing the metadata of the ARMS data collection (dates, locations, IDs, URLS, etc) as provided for the LifeWatch IJI workflow. This includes references to archived sequence data, image data, and spreadsheet data, and thus is a complete overview. As the different steps of the ARMS workflow execute different processes on different data, the actual data to load into any single step will be a subset of this table. Appropriate subsetted template CSV files are also provided here (see the "Subsetted" files described below). As more data become available, new rows will be added to this spreadsheet, so it will be continuously updated (rather than released as new versions). Note that we aim to include a complete overview of the ARMS-MBON data collection in this file, but there may be a lag between updates. 
* [ARMS4Tesseract_metadata.csv](https://raw.githubusercontent.com/arms-mbon/Data/main/LifeWatch/ARMS4Tesseract_metadata.csv): a description of the columns in the data file (ARMS_Samples_IJI.csv), including the datatype and propertyURL. These are provided to help developers understand what is contained in the columns. 
* [ARMS4Tesseract.ttl](https://raw.githubusercontent.com/arms-mbon/Data/main/LifeWatch/ARMS4Tesseract.ttl) and [ARMS4Tesseract.ldt](https://raw.githubusercontent.com/arms-mbon/Data/main/LifeWatch/ARMS4Tesseract.ldt) are the same data as in ARMS4Tesseract_data.csv, but are in are formats for developer-focussed access. 


**Subsetted files** 

We have subsetted the ARMS4Tesseract_data.csv so that we can provide templates for the separate paths of the IJI workflow. These files are:
* [ARMS4Tesseract_PEMA_data.csv](https://raw.githubusercontent.com/arms-mbon/Data/main/LifeWatch/ARMS4Tesseract_PEMA_data.csv), [ARMS4Tesseract_PEMA_metadata.csv](https://raw.githubusercontent.com/arms-mbon/Data/main/LifeWatch/ARMS4Tesseract_PEMA_metadata.csv): a template of the table that the workflow should present to users who want to run the PEMA path of the workflow. Note that the metadata file includes two extra columns to suggest column titles that should be used in the Tesseract's workflow input table, and a the ordering for the columns in that table
<!--
* ARMS4IJI_Template4Images_data.csv, ARMS4IJI_Template4Images_metadata.csv: is a template of the table that the workflow should present to users who want to run the Image analysis path of the workflow (which does not yet exist). Note that the metadata files includes additional information to that taken from the overview file (ARMS_Samples_IJI_description.csv), to carry information specific to displaying the data in the table in the Tesseracto workflow
* ARMS4IJI_Template4ManualObs_data.csv, ARMS4IJI_Template4ManualObs_metadata.csv: is a template of the table that the workflow should present to users who want to run the manual observations path of the workflow (which does not yet exist). Note that the metadata files includes additional information to that taken from the overview file (ARMS_Samples_IJI_description.csv), to carry information specific to displaying the data in the table in the Tesseracto workflow
-->

**Information on ARMS4Tesseract_data.csv**
* Each row in ARMS4Tesseract_data.csv is for the datasets linked to a particular sampling event: as several datasets (sequences, images, and/or manual observations) are linked to each sampling event, each sampling event has several associated rows, each with a unique sampleID. 
* The columns called _gene_COI|18S|ITS_ and _negativeControl_gene_COI|18S|ITS_ contain the run accession numbers of the associated raw sequences that are archived in [ENA](https://www.ebi.ac.uk/ena/browser/home)
    * In order to view the ENA run accession webpage for any sequence, you need to go to https<nowiki>://www<nowiki>.ebi<nowiki>.ac<nowiki>.uk/ena/browser/view/{cell value} 
    * In order to automatically download the two fastq files for each of the run accession numbers, you can use the webservices as documented on https://github.com/enasequence/enaBrowserTools, e.g. enaDataGet -f fastq -d /tmp/ run ERR3460470 (with "ERR3460470" being the accession number)
    * NA means that there is no link (i.e. "not present"), usually because that row is not describing sequences but rather the images or manual observations
* The column called _OtherDataLink_ contains the URI to the zip files that hold the ARMS images or to the CSV files of manual observations
    * In order to download those files directly, the URL is https<nowiki>://mda<nowiki>.vliz<nowiki>.be/download.php?file={cell value}
    * To view a webpage with the  metadata of the files and from where the data can be downloaded manually, the URL is https<nowiki>://mda<nowiki>.vliz<nowiki>.be/directlink.php?fid={cell value}
    * NA means that there is no link (i.e. "not present"), usually because that row is not describing images or manual observations, but rather sequences
    * Note that at present the images are wrapped in a ZIP file, and it is still to be decided how these will be incorporated in the ARMS workflow. Once decisions have been made, updates here will follow. 
* The column called _AccessRights_ gives the data licence. This information can be displayed to users as-is (no need to turn the values into a URL, for example). Data which are ClosedAccess cannot be accessed unless the user has permissions (e.g. has the uname and psswd of the ARMS ENA account).   
* The column called _AssociatedFileType_ is to help the IJI developers understand the type of data that are linked to each row. 
   * sequences - the associated data are the sequences in ENA
   * images - the data are images, stored as a single ZIP file, in MDA
   * manual observations - the data are CSV files containing manual observations, provided either as a single CSV or a zip

**Information on ARMS4Tesseract_PEMA_data/metadata.csv**
   
These two files are copies of ARMS4Tesseract_data/metadata.csv: the only differences are
   * The rows not relating to sequence data have been removed
   * The columns containing gene_types that PEMA cannot process (if there are any) have been removed 
   * Two columns have been removed: OtherDataLink and AssociatedFileType as these are no longer necessary in this file
   * Two columns have been added to the metadata file: ColumnTitle_4Tesseract to suggest a column title that can be used and ColumnOrder_4Tesseract that can be used to order the sequences-selection table in the workflow
   
  



