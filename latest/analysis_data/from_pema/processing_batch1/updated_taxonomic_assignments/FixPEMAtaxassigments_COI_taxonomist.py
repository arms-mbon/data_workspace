# Code to take the PEMA 2.1.4 COI extended_final_tables, which only have the NBCI IDs to genus level, 
# and add the species level taxonomy name taken from the tax_assignments files, then adding the 
# associated NCBI ID
# As COI has a clean, regular 7-level taxonomy, this is straightfoward 

import os
import sys
import csv 
import pandas as pd
import re
import json
import requests
import time 
# for NCBI part
from argparse import Namespace
from copy import deepcopy
import sys
import ncbitaxonomist.groupmanager
import ncbitaxonomist.log.logger
import ncbitaxonomist.mapper
import ncbitaxonomist.collector
import ncbitaxonomist.ncbitaxonomist
import ncbitaxonomist.parser.arguments
import ncbitaxonomist.payload.accession
import ncbitaxonomist.payload.name
import ncbitaxonomist.payload.taxid
import ncbitaxonomist.resolve.resolver
import ncbitaxonomist.subtree.subtreeanalyzer
import ncbitaxonomist.utils

# From infile2 read the ASV ID (col 0) and the tab-separated 7 level tax class 
# The ID consists of string_#[###..] and it is the string part that should be matched to that from infile 1
# The taxonomic classification is a series of (tab-separated) columns given as
#    Eukaryota, decimal_number, taxon node (Annelida), decimal_number, taxon node (Polychaeta), decimal_number, taxon_node (Phyllodocida), a_letter (g), decimal_number, taxon_node (Nereididae), decimal_number, taxon_node (Alitta), decimal_number, species (Alitta_virens), decimal_number
# where decimal_number is e.g. 1.0 and example values are given in (). The last name is species
#
# From infile1 read the ASV ID (col 0) and the rest of the row, replacing only the penultimate and final 
# columns with that tax classification and NCBI ID extracted from infile2. 
#

# Get relative current location by looking at the path of the script
location = os.path.dirname(os.path.realpath(sys.argv[0]))
infiles1 = ["Extended_final_table_ARMS_Gdynia_GDY1_20180813_20191029_SF38_DMSO_COI_noBlank.csv", "Extended_final_table_April2021_COI_noBlank.csv", "Extended_final_table_August2023_COI_noBlank.csv", "Extended_final_table_January2020_COI_noBlank.csv", "Extended_final_table_January2022_COI_noBlank.csv", "Extended_final_table_July2019_COI_noBlank.csv", "Extended_final_table_May2021_COI_noBlank.csv", "Extended_final_table_September2020_COI_noBlank.csv"]
infiles2 = ["tax_assignments_ARMS_Gdynia_GDY1_20180813_20191029_SF38_DMSO_COI_noBlank.tsv","tax_assignments_April2021_COI_noBlank.tsv","tax_assignments_August2023_COI_noBlank.tsv","tax_assignments_January2020_COI_noBlank.tsv","tax_assignments_January2022_COI_noBlank.tsv","tax_assignments_July2019_COI_noBlank.tsv","tax_assignments_May2021_COI_noBlank.tsv","tax_assignments_September2020_COI_noBlank.tsv"]
outfiles = ["Extended_final_table_ARMS_Gdynia_GDY1_20180813_20191029_SF38_DMSO_COI_noBlank_TaxonomyFull.csv", "Extended_final_table_April2021_COI_noBlank_TaxonomyFull.csv", "Extended_final_table_August2023_COI_noBlank_TaxonomyFull.csv", "Extended_final_table_January2020_COI_noBlank_TaxonomyFull.csv", "Extended_final_table_January2022_COI_noBlank_TaxonomyFull.csv", "Extended_final_table_July2019_COI_noBlank_TaxonomyFull.csv", "Extended_final_table_May2021_COI_noBlank_TaxonomyFull.csv", "Extended_final_table_September2020_COI_noBlank_TaxonomyFull.csv"]
logfile = "FixPEMAtaxassignments_COI_taxonomist_logfile.txt"
asvid_vs_taxclass = {} # a dictionary to hold the asvids as key and the tax classification + ncbiid
asvid_vs_ncbiid = {}
ranksin = ["kingdom","phylum", "class", "order", "family", "genus", "species"]


# The function to get the NCBI ID for a name. 
def resolve(name):
    args = Namespace()
    args.version = False
    args.verbose = 0
    args.apikey = None
    args.command = "resolve"
    args.taxids = None
    args.names = [name]
    args.database = None
    args.remote = True
    args.email = None
    args.xml = False
    args.mapping = False
    sys_exit_copy = deepcopy(sys.exit)
    sys.exit = lambda *args, **kwargs: None
    ncbi_id = -999999
    try:
        ncbitaxonomist.ncbitaxonomist.configure(args)
        nt = ncbitaxonomist.ncbitaxonomist.NcbiTaxonomist(args.database)
        txresolver = ncbitaxonomist.resolve.resolver.Resolver(nt)
        txresolver.cache.taxa.taxa = {}
        txresolver.resolve(
            taxids=ncbitaxonomist.payload.taxid.TaxidPayload(args.taxids),
            names=ncbitaxonomist.payload.name.NamePayload(args.names),
            mapping=args.mapping,
            remote=args.remote,
        )
        ncbi_id = [k for k, _ in txresolver.cache.taxa.taxa.items()][0]
        sys.exit = sys_exit_copy
        return ncbi_id
    except Exception:
        sys.exit = sys_exit_copy
        return ncbi_id

writelog = open(logfile,"w")
dictofnames = {} # to hold the names and IDs so that one does not need to repeat taxonomist searches
for i in range(len(outfiles)):
    infile1 = infiles1[i]
    infile2 = infiles2[i]
    outfile = outfiles[i]
    # filling the dictionary from infile2 - ASVID with tax class and ASVID with NCBIID
    with open(infile2, 'r') as csvfile2:
        print("----->Processing ",infile2)
        reader = csv.reader(csvfile2, delimiter='\t')   
        irow = 0
        for row in reader:
            #if irow % 100 == 0: print("....row",irow)
            irow+=1
            id = row[0].split("_")[0]
            taxclass = row[1]+";"+row[4]+";"+row[7]+";"+row[10]+";"+row[13]+";"+row[16]+";"+row[19].replace("_"," ")
            asvid_vs_taxclass[id] = taxclass
            # now need the new tax classification to go into the new extended final table
            taxclasslist = [row[1],row[4],row[7],row[10],row[13],row[16],row[19].replace("_"," ")]
            # now have to do backwards NCBI search on the scientific name until get a match
            fuck = 0
            for mm in reversed(taxclasslist):
                if fuck == 0:
                    ncbiid = "No match"
                    if mm != "NA":
                        if mm in dictofnames.keys():
                            ncbiid = dictofnames[mm]
                            print("-----used existing")
                            fuck = 1
                        else:
                            time.sleep(1)
                            sey = resolve(mm)
                            if sey == -999999:
                                fuck = 0
                                L = "file:"+infile1+" row:"+str(irow)+" otu:"+id+" name:"+mm+" "+str(sey)+" \n"
                                writelog.write(L) # filename, row number, row Id, name that failed
                            else:
                                sey = sey
                                ncbiid = mm+":"+str(sey) 
                                dictofnames[mm] = ncbiid 
                                fuck = 1
                    asvid_vs_ncbiid[id]=ncbiid 
    # now read each line in infile1 and write to outfile with the extra info from infile2
    with open(outfile, 'w', newline='') as csvfileout:
        writer = csv.writer(csvfileout, delimiter=',')
        print("---->Processing ",outfile)
        with open(infile1, 'r') as csvfile1:
            reader = csv.reader(csvfile1, delimiter=',')   
            irow = 0 
            for row in reader:
                if irow == 0: 
                    writer.writerow(row)
                else:
                    id = row[0].split(":")[1]
                    row[-2] = asvid_vs_taxclass.get(id,"Not found")
                    row[-1] = asvid_vs_ncbiid.get(id,"Not found")
                    writer.writerow(row)
                if irow % 100 == 0: print("....row",irow)
                irow+=1
print("THE END")