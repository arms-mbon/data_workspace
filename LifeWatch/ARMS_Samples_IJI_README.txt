ARMS_Samples_IJI.csv: the CSV file containing all the metadata of the ARMS data collection (dates, locations, IDs, URLS, etc) 
ARMS_Samples_IJI_description.csvw.jsonld: jsonld version of that, to allow developers to access these metadata m2m
 
Pay Attention:

- Each row in ARMS_Samples_IJI.csv is a single material sample, and there can be several rows for each sampling event. 
- The columns called gene_COI|18S|ITS and negativeControl_gene_COI|18S|ITS contain the ENA run accession numbers of raw sequences
    - In order to VIEW the webpage on ENA for those sequences, you need to go to https://www.ebi.ac.uk/ena/browser/view/{cell value}
    - In order to automatically DOWNLOAD the 2 fastq files for each of the run accesion numbers, you can use the webservices as documented on https://github.com/enasequence/enaBrowserTools, e.g. enaDataGet -f fastq -d /tmp/ run ERR3460470 (the ERR## is the value in the cells)
- The column called OtherDataLink contains the URI of zip files of image or CSV files of manual observations, currently
    - In order to download those files directly, the URL is https://mda.vliz.be/download.php?file={cell value}
    - In order to allow a user to see the metadata of the files and download manually, the URL is https://mda.vliz.be/directlink.php?fid={cell value}
    - NA means that there is no link (i.e. "not present")
    Note that this column is NOT NECESSARY TO INCLUDE in the table in the workflow for the step "select sequences"  
- The column called AccessRights is there because for some rows of ARMS_Samples_IJI.csv, the data are only open to ARMS.  
- The column called AssociatedFileType is to help the developers understand the type of data that are linked to each row. In this way you can decide whether the row needs to be included in the table: a table that is for selecting sequences only needs the rows with value "sequences" in this column; a table that is for selecting images or manual observations (not currently part of the workflow) similarly needs only the row with value "images" or "manual observations" in the row. 
   - sequences - the associated data are the sequences in ENA
   - images - the data are images, stored as a single ZIP file, in MDA
   - manual observations - the data are CSV files containing manual observations, provided either as a single CSV or a zip
 
  Correct as of March 29 2022
