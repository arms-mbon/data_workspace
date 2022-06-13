Here we have placed all the data that the LifeWatch Tesseracto ARMS workflow requires.

* ARMS_Samples_IJI.csv: the CSV file containing all the metadata of the ARMS data collection (dates, locations, IDs, URLS, etc). Note that this includes references to archived sequence data, image data, and spreadsheet data, and thus is a complete overview. As the different steps of the ARMS workflow execute different processes on different data, the actual data to load into any single step will be a subset of this table. Appropriate subsetted template CSV files are also provided here (see the "Template" files described below).  
* ARMS_Samples_IJI_description.csv: a description of the columns in the data file (ARMS_Samples_IJI.csv), including the datatype and propertyURL. These are provided to help developers understand what is contained in the columns. 
* ARMS_Samples_IJI.ttl and ARMS_Samples_IJI_template_ldt are formats for developer-focussed access.

We have subsetted the ARMS all-data file (ARMS_Samples_IJI.csv) so that we can provide a template of the data to load  and the data-selection-table to present in the different paths of the ARMS workflow. These currently include:
* ARMS4IJI_Template4PEMA_data.csv, ARMS4IJI_Template4PEMA_metadata.csv: a template of the table that the workflow should present to users who want to run the PEMA arm of the workflow. Note that the metadata files includes additional information to that taken from the overview file (ARMS_Samples_IJI_description.csv), to carry information specific to displaying the data in the table in the Tesseracto workflow
* ARMS4IJI_Template4Images_data.csv, ARMS4IJI_Template4Images_metadata.csv: is a template of the table that the workflow should present to users who want to run the Image analysis arm of the workflow (which does not yet exist). Note that the metadata files includes additional information to that taken from the overview file (ARMS_Samples_IJI_description.csv), to carry information specific to displaying the data in the table in the Tesseracto workflow
* ARMS4IJI_Template4ManualObs_data.csv, ARMS4IJI_Template4ManualObs_metadata.csv: is a template of the table that the workflow should present to users who want to run the manual observations arm of the workflow (which does not yet exist). Note that the metadata files includes additional information to that taken from the overview file (ARMS_Samples_IJI_description.csv), to carry information specific to displaying the data in the table in the Tesseracto workflow

**Information on ARMS_Samples_IJI.csv**
* Each row in ARMS_Samples_IJI.csv is a single material sample, and there can be several rows for each sampling event as each row corresponds to a unique (sequence, image, or manual observation) dataset from that sampling event. 
* The columns called _gene_COI|18S|ITS_ and _negativeControl_gene_COI|18S|ITS_ contain the ENA run accession numbers of raw sequences
    * In order to view the webpage on ENA for those sequences, you need to go to _https://www.ebi.ac.uk/ena/browser/view/{cell value}_
    * In order to automatically download the two fastq files for each of the run accesion numbers, you can use the webservices as documented on https://github.com/enasequence/enaBrowserTools, e.g. enaDataGet -f fastq -d /tmp/ run ERR3460470 (the ERR## is the value in the cells)
    * The PEMA workflow requires the ENA accesion numbers only, not an actual download of the data
* The column called _OtherDataLink_ contains the URI of zip files of images or the CSV files of manual observations
    * In order to download those files directly, the URL is _https://mda.vliz.be/download.php?file={cell value}_
    * To load the metadata of the files from which webpage the data can be downloaded manually, the URL is _https://mda.vliz.be/directlink.php?fid={cell value}_
    * NA means that there is no link (i.e. "not present")
    * Note that at present the images are wrapped in a ZIP file, and it is still to be decided how these will be incorporated in the ARMS workflow. Once decisions have been made, updates here will follow. 
* The column called _AccessRights_ gives the data licence. This information can be displayed to users as-is (no need to turn the values into a URL, for example). Data which are ClosedAccess cannot be accessed unless the user has permissions (e.g. has the uname and psswrd of the ARMS ENA account).   
* The column called _AssociatedFileType_ is to help the developers understand the type of data that are linked to each row. 
   * sequences - the associated data are the sequences in ENA
   * images - the data are images, stored as a single ZIP file, in MDA
   * manual observations - the data are CSV files containing manual observations, provided either as a single CSV or a zip

**Information on ARMS4IJI_Template4PEMA_data**
This is a template of the data to load into the PEMA path of the workflow, to present to the user as a selection table. The data and metadata files contain the following: 
* TO BE WRITTEN 


**Information on ARMS4IJI_Template4Images/ManualObs_data**
This is template of the data to load into the Image analysis or Manual Observations analysis paths of the workflow, to present to the user as a selection table. The data and metadata files contain the following: 
* TO BE WRITTEN


TO BE DONE 
* rename ARMS_Samples_IJI.csv to ARMS4Tesseract_data.csv
* rename ARMS_Samples_IJI_description.csv to ARMS4Tesserat_metadata.csv
* appropriately rename the ldt and ttl files
* create the template csv and metadata files
* create the templates' template and ttl files
* in main ARMS input files: - change "gene_COI" to just "COI" and negativeControl_gene_COI to COI (neg. control), change "sequencing pending" to "pending"
* check this statement "The PEMA workflow requires the ENA accesion numbers only, not an actual download of the data"
* turn "open access" into an actual licence


