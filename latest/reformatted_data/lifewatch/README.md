Here we have placed all metadata for the ARMS workflow of the LifeWatch Tesseract. These data are provided for a specific purpose and with a specific layout, and while the data here are openly accessible, this is not the place to look for the overview of the ARMS data if you are coming to this page with that intent. Instead, you should go to [the data workspace](https://github.com/arms-mbon/data_workspace/tree/main/qualitycontrolled_data).

The files used in the PEMA branch of the ARMs workflow in the Tesseract are:
* [ARMS4Tesseract_PEMA_data.csv](https://raw.githubusercontent.com/arms-mbon/Data/main/LifeWatch/ARMS4Tesseract_PEMA_data.csv) contains the ARMS-MBON sampling events that have associated raw sequences archived in ENA (the European Nucleotide Archive). Columns of event and sample metadata, and the 18S, COI, and ITS ENA run accession numbers, can be found here. This data file is turned into a table in the ARMS workflow, from where sequences can be selected to be processed. Each row is linked to a sampling event, and each sampling event can have multiple rows as multiple physical samples were collected for each event. 
* [ARMS4Tesseract_PEMA_metadata.csv](https://raw.githubusercontent.com/arms-mbon/Data/main/LifeWatch/ARMS4Tesseract_PEMA_metadata.csv). The metadata for this data file, giving the data types and data terms for the columns in the data file. Two extra columns are also provided to suggest column titles that should be used in the Tesseract's workflow input table, and a the ordering for the columns in that table

**Some extra information** 

The columns called _gene_COI|18S|ITS_ and _negativeControl_gene_COI|18S|ITS_ contain the run accession numbers of the associated raw sequences that are archived in [ENA](https://www.ebi.ac.uk/ena/browser/home)
* In order to view the ENA run accession webpage for any sequence, you can to go to https<nowiki>://www<nowiki>.ebi<nowiki>.ac<nowiki>.uk/ena/browser/view/{cell value} 
* One way to automatically download the two fastq files for each of the run accession numbers, is to use the webservices as documented on https://github.com/enasequence/enaBrowserTools, e.g. enaDataGet -f fastq -d /tmp/ run ERR3460470 (with "ERR3460470" being the accession number)

The column called _AccessRights_ gives the data licence. Most data are CC BY; ARMS-MBON reserves the right to a 1 year embargo period on the data, and if any of the accession numbers are inaccessible to you, it is probably because of this (however, in our experience, ENA not infrequently has hiccups in providing access to its data, so it is worth trying again a day or two later). Data which are not CC BY cannot be accessed unless the user has permissions (e.g. has the uname and psswd of the ARMS ENA account).   