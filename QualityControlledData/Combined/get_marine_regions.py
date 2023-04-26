import requests
import json
import os
import time

#given a list of lat longs get the marine regions data

base_url = "https://marineregions.org/rest/getGazetteerRecordsByLatLong.json"

#example https://marineregions.org/rest/getGazetteerRecordsByLatLong.json/2/2/?offset=0

#current working directory
curr_dir = os.path.dirname(os.path.realpath(__file__))

def read_mr_file():
    #try and read the open(os.path.join(curr_dir, "marine_regions.json")) file if it exists if not create it and return []
    if os.path.isfile(os.path.join(curr_dir, "marine_regions.json")):
        with open(os.path.join(curr_dir, "marine_regions.json"), "r") as f:
            return json.load(f)
    else:
        with open(os.path.join(curr_dir, "marine_regions.json"), "w") as f:
            json.dump([], f)
            return []

def save_mr_file(data):
    #save the data to the file
    with open(os.path.join(curr_dir, "marine_regions.json"), "w") as f:
        json.dump(data, f)

#import the lat longs from the ./combined_ObservatoryData.csv
with open(os.path.join(curr_dir, "combined_ObservatoryData.csv"), "r") as f:
    lines = f.readlines()
    #get the header
    header = lines.pop(0)
    #get the lat longs
    lat_longs = []
    for line in lines:
        lat_longs.append([line.split(",")[3] , line.split(",")[4]])
        
all_marine_regions = []
for latlon in lat_longs:
    resp = requests.get(base_url + "/" + latlon[0] + "/" + latlon[1] + "/?offset=0")
    #response is in json 
    all_marine_regions.append(resp.json()[0])
    towriteline = [latlon[0], latlon[1], resp.json()[0]["preferredGazetteerName"], resp.json()[0]["MRGID"]]
    time.sleep(3)
    mr_data = read_mr_file()
    mr_data.append(towriteline)
    save_mr_file(mr_data)