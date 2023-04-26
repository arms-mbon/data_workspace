#this script will make api calls to the taxonomy browser and get the data for the taxa
# it will check the additional data accosiated to the taxa to see if there is a worms ids linked to it , if so it will take the worms id and get the data from the worms api
# from this it will get the data for the taxa and the worms id and the data for the worms id
#output is a csv file with the data for the taxa and the worms id and the data for the worms id

import requests
import json
import time
import csv
import os

taxonomy_browser_ids = [
    "368048", #with worms
    "1264966", #with worms
    "345490", #with worms
    "1975556" #without worms
]
current_dir_script = os.path.dirname(os.path.realpath(__file__))
#base url to get html from taxonomy browser https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=368048&lvl=0
def get_html_from_taxonomy_browser(taxonomy_browser_id):
    time.sleep(3)
    url = "https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=" + taxonomy_browser_id + "&lvl=0"
    response = requests.get(url)
    return response.text

def get_rank_from_html(html):
    rank = ""
    if "Rank:" in html:
        #print("found rank")
        #print(html.split("Rank:</b>")[1])
        rank = html.split("Rank:")[1].split("</strong>")[0].split("<strong>")[1].strip()
    return rank

def get_scientific_name_from_html(html):
    scientific_name = ""
    #<title>Taxonomy browser (Liocarcinus holsatus)</title>
    if "<title>Taxonomy browser (" in html:
        #print("found scientific name")
        #print(html.split("Scientific name:</b>")[1])
        scientific_name = html.split("<title>Taxonomy browser (")[1].split(")</title>")[0].strip()
    return scientific_name

def get_aphia_id_from_html(html):
    aphia_id = ""
    if "https://www.marinespecies.org/aphia.php?p=taxdetails&amp;" in html:
        #print("found aphia id")
        #print(html.split("https://www.marinespecies.org/aphia.php?p=taxdetails&amp;")[1])
        aphia_id = html.split("https://www.marinespecies.org/aphia.php?p=taxdetails&amp;")[1].split('"')[0].split("=")[1]
    return aphia_id

def get_data_from_aphia_id(aphia_id):
    time.sleep(3)
    url = "https://www.marinespecies.org/rest/AphiaClassificationByAphiaID/" + aphia_id
    #resposne is json 
    response = requests.get(url)
    return response.text

def check_child_info(child, rows):
    #check if child is an object
    try:
        if len(child["child"]) > 0:
            rows.append([child["AphiaID"], child["rank"], child["scientificname"], child["child"]["AphiaID"]])
            return check_child_info(child["child"], rows)  
    except:
        rows.append([child["AphiaID"], child["rank"], child["scientificname"], ""])
        #print(rows)
        return(rows)

def get_taxonomic_info_from_json(json):
    #for key, value in json.items():
    #convertion to csv [["AphiaID","rank","scientificname","child_id"],[1,"kingdom","animalia",2],[2,"phylum","chordata",3],[3,"class","mammalia",4],[4,"order","carnivora",5],[5,"family","canidae",6],[6,"genus","canis",7],[7,"species","canis lupus",8]]
    return check_child_info(json, [])

def get_aphia_name(json_rows):
    #take last row of json_rows and get the scientific name
    return json_rows[-1][2]

def get_aphia_id(json_rows):
    #take last row of json_rows and get the aphia id
    return json_rows[-1][0]

def get_aphia_rank(json_rows):
    return json_rows[-1][1]
    
for taxonomy_browser_id in taxonomy_browser_ids:
    html = get_html_from_taxonomy_browser(taxonomy_browser_id)
    aphia_id = get_aphia_id_from_html(html)
    
    ncbi_scienctific_name = get_scientific_name_from_html(html)
    ncbi_rank = get_rank_from_html(html)
    
    if aphia_id == "":
        print("no worms id for " + taxonomy_browser_id)
        
        #check if convertion.csv file exists if not create it else append to it
        if not os.path.isfile(current_dir_script + "/convertion.csv"):
            with open(current_dir_script + "/convertion.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerow([ncbi_scienctific_name, ncbi_rank, "", "", ""])
        else:
            with open(current_dir_script + "/convertion.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([ncbi_scienctific_name, ncbi_rank, "", "", ""])
        
        continue
    worms_data = get_data_from_aphia_id(aphia_id)
    #pretty print the json
    json_rows = get_taxonomic_info_from_json(json.loads(worms_data))
    print(json_rows)
    
    aphia_id = get_aphia_id(json_rows)
    aphia_scienctific_name = get_aphia_name(json_rows)
    aphia_rank = get_aphia_rank(json_rows)
    
    headers = ["NCBIScientificName","NCBIScientificRank","aphiaScientificNameID","AphiaScientificName","AphiaScientificNameRank"]
    
    #check if convertion.csv file exists if not create it else append to it
    if not os.path.isfile(current_dir_script + "/convertion.csv"):
        with open(current_dir_script + "/convertion.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerow([ncbi_scienctific_name, ncbi_rank, aphia_id, aphia_scienctific_name, aphia_rank])
    else:
        with open(current_dir_script + "/convertion.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([ncbi_scienctific_name, ncbi_rank, aphia_id, aphia_scienctific_name, aphia_rank])
        




