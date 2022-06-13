Here we have placed all the data that the LifeWatch Tesseracto ARMS workflow requires.

* ARMS_Samples_IJI.csv: the CSV file containing all the metadata of the ARMS data collection (dates, locations, IDs, URLS, etc). Note that this includes references to archived sequence data, image data, and spreadsheet data, and thus is a complete overview. As the different steps of the ARMS workflow execute different processes on different data, the actual data to load into any single step will be a subset of this table. Appropriate subsetted template CSV files are also provided here.  
* ARMS_Samples_IJI_description.csv: a description of the columns in the data file (ARMS_Samples_IJI.csv), including the datatype and propertyURL. These, and in particular the propertyURL, is provided to help developers understand what is contained in the columns. 
* ARMS_Samples_JIJ.ttl and ARMS_Samples_IJI_template_ldt are formats for developers to access the information

We have subsetted the ARMS data input file (ARMS_Samples_IJI.csv) so that they provide a template of the data to load  and the data-selection-table to present, in the different paths of the workflow. These currently include:
* ARMS4IJI_Template4PEMA_data.csv, ARMS4IJI_Template4PEMA_metadata.csv: is a template of the table that the workflow should present to users who want to run the PEMA arm of the workflow. Note that the metadata files includes additional information to that taken from the overview file (ARMS_Samples_IJI_description.csv), to carry information about how to display the data in the table in the Tesseracto workflow
* ARMS4IJI_Template4Images_data.csv, ARMS4IJI_Template4Images_metadata.csv: is a template of the table that the workflow should present to users who want to run the Image analysis arm of the workflow (which does not yet exist). Note that the metadata files includes additional information to that taken from the overview file (ARMS_Samples_IJI_description.csv), to carry information about how to display the data in the table in the Tesseracto workflow
* ARMS4IJI_Template4ManualObs_data.csv, ARMS4IJI_Template4ManualObs_metadata.csv: is a template of the table that the workflow should present to users who want to run the manual observations arm of the workflow (which does not yet exist). Note that the metadata files includes additional information to that taken from the overview file (ARMS_Samples_IJI_description.csv), to carry information about how to display the data in the table in the Tesseracto workflow

**Information on ARMS_Samples_IJI.csv**\n
* Each row in ARMS_Samples_IJI.csv is a single material sample, and there can be several rows for each sampling event. 
* The columns called _gene_COI|18S|ITS_ and _negativeControl_gene_COI|18S|ITS_ contain the ENA run accession numbers of raw sequences
    * In order to VIEW the webpage on ENA for those sequences, you need to go to https://www.ebi.ac.uk/ena/browser/view/{cell value}
    * In order to automatically download the 2 fastq files for each of the run accesion numbers, you can use the webservices as documented on https://github.com/enasequence/enaBrowserTools, e.g. enaDataGet -f fastq -d /tmp/ run ERR3460470 (the ERR## is the value in the cells)
* The column called _OtherDataLink_ contains the URI of zip files of images or the CSV files of manual observations
    * In order to download those files directly, the URL is https://mda.vliz.be/download.php?file={cell value}
    * To load the metadata of the files from which webpage the data can be downloaded manually, the URL is https://mda.vliz.be/directlink.php?fid={cell value}
    * NA means that there is no link (i.e. "not present")
* The column called _AccessRights_ is there because for some rows of ARMS_Samples_IJI.csv, the data are only open to ARMS. This information can be displayed to users as-is (no need to turn the values into a URL, for example)  
* The column called _AssociatedFileType_ is to help the developers understand the type of data that are linked to each row. 
   * sequences - the associated data are the sequences in ENA
   * images - the data are images, stored as a single ZIP file, in MDA
   * manual observations - the data are CSV files containing manual observations, provided either as a single CSV or a zip

**Information on ARMS4IJI_Template4PEMA_data**
For this template of the data to load into the PEMA path of the workflow, to present to the user as a selection table, the data and metadata files contain the following: 
* TO BE WRITTEN 


**Information on ARMS4IJI_Template4Images/ManualObs_data**
For this template of the data to load into the Image analysis or Manual Observations analysis paths of the workflow, to present to the user as a selection table, the data and metadata files contain the following: 
* TO BE WRITTEN


TO BE DONE 
* rename ARMS_Samples_IJI.csv to ARMS4Tesseract_data.csv
* rename ARMS_Samples_IJI_description.csv to ARMS4Tesserat_metadata.csv
* appropriately rename the ldt and ttl files
* create the template csv and metadata files
* create the templates' template and ttl files
* in main ARMS input files: - change "gene_COI" to just "COI" and negativeControl_gene_COI to COI (neg. control), change "sequencing pending" to "pending"


