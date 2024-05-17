# Code to take the PEMA 2.1.4 18S extended_final_tables, regularise (curate) the PR2 taxonomic classification 
# following Nauras Daraghmeh's instructions, and get the NCBI ID for the lowest level for which one exists.    

# general
import os
import sys
import csv 
import pandas as pd
import re
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


#get relative current location by looking at the path of the script
location = os.path.dirname(os.path.realpath(sys.argv[0]))

infiles = ["Extended_final_table_April2021_18S_noBlank.csv","Extended_final_table_January2020_18S_noBlank.csv","Extended_final_table_January2022_18S_noBlank.csv","Extended_final_table_July2019_18S_noBlank.csv","Extended_final_table_May2021_18S_noBlank.csv","Extended_final_table_September2020_18S_noBlank.csv","Extended_final_table_August2023_18S_noBlank.csv","Extended_final_table_ARMS_Gdynia_GDY1_20180813_20191029_SF38_DMSO_18S_noBlank.csv"]
outfiles1 = ["April2021_18S_noBlank_TaxonomyCurated.csv","January2020_18S_noBlank_TaxonomyCurated.csv","January2022_18S_noBlank_TaxonomyCurated.csv","July2019_18S_noBlank_TaxonomyCurated.csv","May2021_18S_noBlank_TaxonomyCurated.csv","September2020_18S_noBlank_TaxonomyCurated.csv","August2023_18S_noBlank_TaxonomyCurated.csv","Gdynia_GDY1_20180813_20191029_SF38_DMSO_18S_noBlank_TaxonomyCurated.csv"]
outfiles2 = ["Extended_final_table_April2021_18S_noBlank_TaxonomyCurated.csv","Extended_final_table_January2020_18S_noBlank_TaxonomyCurated.csv","Extended_final_table_January2022_18S_noBlank_TaxonomyCurated.csv","Extended_final_table_July2019_18S_noBlank_TaxonomyCurated.csv","Extended_final_table_May2021_18S_noBlank_TaxonomyCurated.csv","Extended_final_table_September2020_18S_noBlank_TaxonomyCurated.csv","Extended_final_table_August2023_18S_noBlank_TaxonomyCurated.csv","Extended_final_table_ARMS_Gdynia_GDY1_20180813_20191029_SF38_DMSO_18S_noBlank_TaxonomyCurated.csv"]
#logfile = "FixPEMAtaxassignments_18S_taxonomist_logfile.txt"

# see https://pypi.org/project/ncbi-taxonomist/
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

#writelog = open(logfile,"w") # for sanity checking of results
dictofnames = {} # to hold the names and IDs so that one does not need to repeat taxonomist searches
for i in range(len(infiles)):
    infile = infiles[i]
    outfile1 = outfiles1[i]
    outfile2 = outfiles2[i]
    # Go thru the infile and extract the necessary information
    with open(outfile1, 'w', newline='') as csvfile1, open(outfile2, 'w', newline='') as csvfile2:
        writer1 = csv.writer(csvfile1, delimiter=',')
        writer2 = csv.writer(csvfile2, delimiter=',')
        writer1.writerow(["OTUID","taxonomicClassificationOrig","Domain","Supergroup","Division/Kingdom","Phylum/Class","Level_X","Level_XX","Level_XXX","Level_XXXX","Level_XXXXX","genus_species"])
        with open(infile, 'r') as csvinfile:
            print("Processing ",infile," to ",outfile1)
            reader = csv.reader(csvinfile, delimiter=',')     
            irow=0    
            for row in reader:
                if irow == 0:
                    writer2.writerow(row) # header
                else:
                    id = row[0]
                    taxclass = row[-2]
                    # now need to split the taxclass into its elements and tidy up the levelts
                    nodes = taxclass.split(";")
                    sey=0
                    for node in nodes:
                        # then, for each element in that list, 
                        #if "(" in node: node = node.split("(")[0] # was not in Nauras' original code so I will remove here also 
                        if "clade" in node: node = node.replace("clade","Clade")
                        if "var." in node: node = "var."
                        if " " in node: node = "NA"
                        if "X " in node: node = "NA"
                        if "XX" in node: node = "NA"
                        if "sp." in node: node = "NA"
                        #if "Unknown" in node: node = "NA" # was not in Nauras' original code so I will remove here also
                        if sey == 0: 
                            taxclass_cln = node
                        else:
                            if node != "NA":   
                                taxclass_cln += ";"
                                taxclass_cln += node
                        sey += 1  
                    # now fill in the taxclass so there are 10 levels, filling in with NA where those levels are blank
                    # then for the last entry, if there is a species name (lower case), replace the NA with genus_species
                    taxclass_cln2 = ["NA"] * 10
                    nodes = taxclass_cln.split(";")
                    # the first value of nodes is always "NA", which comes from the "Main genome" in the input, and we do not need this
                    nodes.pop(0)
                    nlen = len(nodes)
                    for j in range(nlen):
                        taxclass_cln2[j]=nodes[j] 
                        # here we are assuming that really all lower-cases are species and that this never occurs in the first element
                        # at same time, set assignments containing "lineage" string in Species column as NA
                        if node.islower():
                            sey = nodes[j-1] + "_" + nodes[j]
                            if "lineage" in sey: sey = "NA"
                            taxclass_cln2[9] = sey
                    # Now need to get the NCBI ID for the last name in the list, moving backwards until have one
                    # Check first if the value was already added to our dictionary
                    fuck = 0
                    for mm in reversed(taxclass_cln2):
                        if fuck == 0:
                            ncbiid = "Not resolved"
                            if mm != "NA":
                                if mm in dictofnames.keys():
                                    ncbiid = dictofnames[mm]
                                    fuck = 1
                                else:
                                    time.sleep(2)
                                    sey = resolve(mm)
                                    if sey == -999999:
                                        #L = "file:"+infile+" row:"+str(irow)+" otu:"+id+" name:"+mm+" "+str(sey)+" \n"
                                        #writelog.write(L) # filename, row number, row Id, name that failed
                                        fuck = 0
                                    else: 
                                        ncbiid = mm+":"+str(sey) 
                                        dictofnames[mm] = ncbiid
                                        fuck = 1
                    # Now write out a copy of the extended final table
                    writer1.writerow([id,taxclass,taxclass_cln2[0],taxclass_cln2[1],taxclass_cln2[2],taxclass_cln2[3],taxclass_cln2[4],taxclass_cln2[5],taxclass_cln2[6],taxclass_cln2[7],taxclass_cln2[8],taxclass_cln2[9]])
                    sey = "Main genome;"+taxclass_cln2[0]+";"+taxclass_cln2[1]+";"+taxclass_cln2[2]+";"+taxclass_cln2[3]+";"+taxclass_cln2[4]+";"+taxclass_cln2[5]+";"+taxclass_cln2[6]+";"+taxclass_cln2[7]+";"+taxclass_cln2[8]+";"+taxclass_cln2[9]
                    row[-2] = sey
                    row[-1] = ncbiid
                    writer2.writerow(row) 
                irow+=1

#writelog.close()
print("THE END")