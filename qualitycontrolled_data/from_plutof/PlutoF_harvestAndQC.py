# do imports
import sys
import os
import time
import json
import csv
import requests
import shutil
import uritemplate
import csv
import re

# from dotenv import load_dotenv
import pandas as pd

# variables here
# import json file names ./ARMS_data.json
# get parent dir of current file
parent_dit = os.path.dirname(os.path.abspath(__file__))
output_dir = parent_dit

# download the plutoF josn dump
# plutoF_url_dmp = "https://files.plutof.ut.ee/orig/3499F3A9B37BD8DA30F60A8CBE22580C403269818043A9324758C3F84434BAEB.json?h=hW-cqCf3zI5m7Yv6Vg1gJA&e=1709216887"
plutoF_json_dmp = os.path.join(output_dir, "AllARMSPlutof.json")
# download the plutoF josn dump
# file_dump = requests.get(plutoF_url_dmp, allow_redirects=True)
# pyt the file dump in the output dir
# with open(plutoF_json_dmp, "wb") as f:
#    f.write(file_dump.content)

# load json file
json_data = open(os.path.join(parent_dit, "AllARMSPlutof.json"))
json_data_loaded = json.load(json_data)

# load in csv file PlutoF_QC_v2_StationARMSnames.csv
with open(os.path.join(parent_dit, "PlutoF_QC_StationARMSnames.csv"), "r") as f:
    qc_stations = list(csv.reader(f))
# print(qc_stations)

# variables that will make the csv files
csv_file_QC_output = []


# helper function that will convert input date format 2021-05-15 18:53:34.831045+00:00 to format 2021-05-15
def converteddate(date):
    try:
        new_date = date.split(" ")[0]
        return new_date
    except:
        return date


def getPlateNumberAndPosition(file_name):
    # do a regular expression to get the plate position and plate number the expression should search for "_1-9(B or T)" eg _1T_ or _2B_ or _3B_
    # the regex should find patterns like: _1T_ or _2B_ or _3B_
    regex = re.compile(r"_(\d)([BT])")
    found = regex.search(file_name)
    # check if the regex found a match and if so return the match
    if found:
        # print(found.group(1))
        # print(found.group(2))
        if found.group(2) == "T":
            return found.group(1), "Top"
        elif found.group(2) == "B":
            return found.group(1), "Bottom"
    else:
        return "Not Provided", "Not Provided"


def getDepthMax(child_area):
    # check if measurements are presentr in the child area
    try:
        if child_area["measurements"]:
            # loop over the measurements and check if measurements[i]['measurement][name] == 'Depth max'
            i = 0
            for measurements in child_area["measurements"]:
                if measurements["measurement"]["name"] == "Depth max":
                    # if so return the measurement value
                    return child_area["measurements"][i]["value"]
                i += 1
        else:
            return "no measurements"
    except:
        return "no measurements"


def getDepthMin(child_area):
    try:
        if child_area["measurements"]:
            # loop over the measurements and check if measurements[i]['measurement][name] == 'Depth max'
            i = 0
            for measurements in child_area["measurements"]:
                if measurements["measurement"]["name"] == "Depth min":
                    # if so return the measurement value
                    return child_area["measurements"][i]["value"]
                i += 1
        else:
            return "no measurements"
    except:
        return "no measurements"


# helper functions that takes in input and also input column and return the value of the "input column corrected" from the qc-stations csv file if the value is not blank
def correctedvalue(input_value, input_column, input_country=None, input_station=None):
    index_column = 0
    print(f"input value: {input_value}")
    print(f"input column: {input_column}")
    print(f"input country: {input_country}")
    print(f"input station: {input_station}")
    for field in qc_stations[0]:
        print(f"field: {field}")
        if field == input_column + " in plutof":
            tocheckcolumn = index_column
        if field == input_column + " corrected":
            correctedcolumn = index_column
        index_column += 1

    print(f"tocheckcolumn: {tocheckcolumn}")

    toreturn = input_value
    found_station = False
    for row in qc_stations:
        if row[tocheckcolumn] == input_value:
            found_station = True
            if (
                row[correctedcolumn] != ""
                and row[correctedcolumn] != " "
                and row[correctedcolumn] != None
            ):
                correction_found = True
                # print(f'corrected value found for {input_value} in {input_column} column => {row[correctedcolumn]}')
                toreturn = row[correctedcolumn]
                # add to csv file
                if input_column == "Country":
                    csv_file_QC_output.append(
                        {
                            "station": "NA",
                            "country": toreturn,
                            "unit": "NA",
                            "qc_param": input_column,
                            "qc_flag": "passed",
                        }
                    )
                elif input_column == "Station":
                    csv_file_QC_output.append(
                        {
                            "station": toreturn,
                            "country": input_country,
                            "unit": "NA",
                            "qc_param": input_column,
                            "qc_flag": "passed",
                        }
                    )
                elif input_column == "ARMS unit":
                    csv_file_QC_output.append(
                        {
                            "station": input_station,
                            "country": input_country,
                            "unit": toreturn,
                            "qc_param": input_column,
                            "qc_flag": "passed",
                        }
                    )
            else:
                # print('no corrected value for ' + input_value)
                toreturn = input_value

    if found_station == False:
        correction_found = True
        if input_column == "Station":
            csv_file_QC_output.append(
                {
                    "station": input_value,
                    "country": input_country,
                    "unit": "NA",
                    "qc_param": input_column,
                    "qc_flag": "missing",
                }
            )
        elif input_column == "Country":
            csv_file_QC_output.append(
                {
                    "station": "NA",
                    "country": input_value,
                    "unit": "NA",
                    "qc_param": input_column,
                    "qc_flag": "missing",
                }
            )
        elif input_column == "ARMS unit":
            csv_file_QC_output.append(
                {
                    "station": input_station,
                    "country": input_country,
                    "unit": input_value,
                    "qc_param": input_column,
                    "qc_flag": "missing",
                }
            )
    return toreturn


# get the following variables from the json file
# sampling areas ids
sampling_areas_ids = []
# child_areas_ids
child_areas_ids = []
# get all sampling_event_ids
sampling_event_ids = []
for sampling_area in json_data_loaded["sampling_areas"]:
    sampling_areas_ids.append(sampling_area["id"])
    for child_area in sampling_area["child_areas"]:
        child_areas_ids.append(child_area["id"])
        for sampling_event in child_area["sampling_events"]:
            sampling_event_ids.append(sampling_event["id"])

# make the following csv files
# Main.csv => Station, Country, ARMS_unit, Date_start, Date_end, Event_description, Material Samples, Observations, Sequences, Associated Date, Created, Updated
main_csv_data = []
sequences_csv_data = []
associated_csv_data = []
observations_csv_data = []
material_samples_csv_data = []
correction_found = False
# make sample area name by replcing space with underscore
for sampling_area in json_data_loaded["sampling_areas"]:
    ew_sampling_area_name = sampling_area["name"].replace(" ", "_")
    material_samples_csv = []
    observations_csv = []
    sequences_csv = []
    associated_data_csv = []
    main_data_csv = []
    try:
        os.mkdir(os.path.join(output_dir, ew_sampling_area_name))
    except Exception as e:
        print(e)
    # country
    country = correctedvalue(sampling_area["country"], "Country")

    station = correctedvalue(
        sampling_area["name"], "Station", input_country=sampling_area["country"]
    )
    # print(f"working on {sampling_area['name']}")
    # print(f'working on {station}')
    for child_area in sampling_area["child_areas"]:
        # print(f" area name {child_area['name']}")
        pre_ARMS_unit = correctedvalue(
            child_area["name"],
            "ARMS unit",
            input_country=country,
            input_station=station,
        )
        if pre_ARMS_unit == " " or pre_ARMS_unit == "" or pre_ARMS_unit == None:
            pre_ARMS_unit = child_area["name"]
        # print(pre_ARMS_unit)
        # pre_ARMS_unit = pre_ARMS_unit.replace(station,'')
        pre_ARMS_unit = pre_ARMS_unit.replace("_", "")
        pre_ARMS_unit = pre_ARMS_unit.replace("ARMS", "")
        ARMS_unit = pre_ARMS_unit

        # get latitude longitude and depth
        latitude = child_area["latitude"]
        longitude = child_area["longitude"]
        depth_max = getDepthMax(child_area)
        depth_min = getDepthMin(child_area)

        if depth_max == "no measurement" and depth_min != "no measurement":
            depth_max = depth_min

        if depth_min == "no measurement" and depth_max != "no measurement":
            depth_min = depth_max

        # RavHarbour RavH3 caviat to fix
        if depth_min == "no measurement" and depth_max == "no measurement":
            depth_max = "1.5"
            depth_min = "1.5"

        for sampling_event in child_area["sampling_events"]:
            # date_start
            date_start = converteddate(sampling_event["timespan_begin"])
            # date_end
            date_end = converteddate(sampling_event["timespan_end"])
            # event_id
            event_id = sampling_event["id"]

            # get the habitat data

            habitat = sampling_event["habitat"]

            # try and get the desciption and iucn_habitat_type
            try:
                description = habitat["description"]
            except:
                description = "NA"

            try:
                iucn_habitat_type = habitat["iucn_habitat_type"]
            except:
                iucn_habitat_type = "NA"

            # event_description
            try:
                try:
                    date_end_desc = date_end.replace("-", "")
                    if len(date_end.replace("-", "")) != 8:
                        date_end_desc = "00000000"
                except:
                    date_end_desc = "00000000"

                try:
                    date_start_desc = date_start.replace("-", "")
                    if len(date_start.replace("-", "")) != 8:
                        date_start_desc = "00000000"
                except:
                    date_start_desc = "00000000"

                event_description = (
                    "ARMS_"
                    + station
                    + "_"
                    + ARMS_unit
                    + "_"
                    + date_start_desc
                    + "_"
                    + date_end_desc
                )
            except:
                event_description = (
                    "ARMS_"
                    + station
                    + "_"
                    + ARMS_unit
                    + "_"
                    + "00000000"
                    + "_"
                    + "00000000"
                )
            # material_samples
            material_samples = len(sampling_event["material_samples"])
            # observations
            observations = len(sampling_event["observations"])
            # sequences
            sequences = len(sampling_event["sequences"])
            # associated_date
            associated_date = len(sampling_event["files"])
            # created
            created = converteddate(sampling_event["created_at"])
            # updated
            updated = converteddate(sampling_event["updated_at"])

            # material_sample table here
            for material_sample in sampling_event["material_samples"]:
                sample_id = material_sample["id"]
                sample_description = material_sample["description"]
                material_sample_id = material_sample["name"]
                sample_id_created_at = converteddate(material_sample["created_at"])
                sample_id_updated_at = converteddate(material_sample["updated_at"])
                sequences_in_sample = 0
                for sequence in sampling_event["sequences"]:
                    if sequence["object_id"] == sample_id:
                        sequences_in_sample += 1
                material_samples_csv.append(
                    {
                        "Material_Sample_ID": material_sample_id,
                        "Parent_Event_ID": event_description,
                        "Description": sample_description,
                        "Created_At": sample_id_created_at,
                        "Updated_At": sample_id_updated_at,
                        "Sequences": sequences_in_sample,
                        "Associated data": associated_date,
                    }
                )
                material_samples_csv_data.append(
                    {
                        "Material_Sample_ID": material_sample_id,
                        "Parent_Event_ID": event_description,
                        "Description": sample_description,
                        "Created_At": sample_id_created_at,
                        "Updated_At": sample_id_updated_at,
                        "Sequences": sequences_in_sample,
                        "Associated data": associated_date,
                    }
                )

            # observation table here
            for observation in sampling_event["observations"]:
                observation_id = observation["id"]
                observation_remarks = observation["remarks"]
                observation_is_varified = observation["moderation_status"]
                for determination in observation["determinations"]:
                    observation_updated_at = converteddate(determination["updated_at"])
                    observation_created_at = converteddate(determination["created_at"])
                    taxon_name = determination["taxon_node"]
                    observations_csv.append(
                        {
                            "Station": station,
                            "Country": country,
                            "ARMS_unit": ARMS_unit,
                            "date_start": date_start,
                            "date_end": date_end,
                            "Event_id": event_description,
                            "Remarks": observation_remarks,
                            "Is_Varified": observation_is_varified,
                            "Taxon_Name": taxon_name,
                            "created_at": observation_created_at,
                            "updated_at": observation_updated_at,
                        }
                    )
                    observations_csv_data.append(
                        {
                            "Station": station,
                            "Country": country,
                            "ARMS_unit": ARMS_unit,
                            "date_start": date_start,
                            "date_end": date_end,
                            "Event_id": event_description,
                            "Remarks": observation_remarks,
                            "Is_Varified": observation_is_varified,
                            "Taxon_Name": taxon_name,
                            "created_at": observation_created_at,
                            "updated_at": observation_updated_at,
                        }
                    )

            # sequences table here
            for sequence in sampling_event["sequences"]:
                sequence_id = sequence["id"]
                sequence_updated_at = converteddate(sequence["updated_at"])
                sequence_created_at = converteddate(sequence["created_at"])
                sequence_sequence = sequence["sequence"]
                sequence_chimeric = sequence["chimeric_status"]
                sequence_unite_status = sequence["unite_status"]
                sequence_low_quality = sequence["quality_status"]
                sequence_forward_primer = sequence["forw_primer_sequence"]
                sequence_reverse_primer = sequence["rev_primer_sequence"]
                sequence_remarks = sequence["remarks"]
                sequence_regions = ";".join(sequence["regions"])
                sequences_csv.append(
                    {
                        "Station": station,
                        "Country": country,
                        "ARMS_unit": ARMS_unit,
                        "date_start": date_start,
                        "date_end": date_end,
                        "Event_id": event_description,
                        "Sequence_ID": sequence_id,
                        "Sequence": sequence_sequence,
                        "Chimeric": sequence_chimeric,
                        "Unite_Status": sequence_unite_status,
                        "Low_Quality": sequence_low_quality,
                        "Forward_Primer": sequence_forward_primer,
                        "Reverse_Primer": sequence_reverse_primer,
                        "Remarks": sequence_remarks,
                        "Regions": sequence_regions,
                        "created_at": sequence_created_at,
                        "updated_at": sequence_updated_at,
                    }
                )
                sequences_csv_data.append(
                    {
                        "Station": station,
                        "Country": country,
                        "ARMS_unit": ARMS_unit,
                        "date_start": date_start,
                        "date_end": date_end,
                        "Event_id": event_description,
                        "Sequence_ID": sequence_id,
                        "Sequence": sequence_sequence,
                        "Chimeric": sequence_chimeric,
                        "Unite_Status": sequence_unite_status,
                        "Low_Quality": sequence_low_quality,
                        "Forward_Primer": sequence_forward_primer,
                        "Reverse_Primer": sequence_reverse_primer,
                        "Remarks": sequence_remarks,
                        "Regions": sequence_regions,
                        "created_at": sequence_created_at,
                        "updated_at": sequence_updated_at,
                    }
                )

            # associated_data table here
            for file in sampling_event["files"]:
                file_name = str(file["id"])
                platenumber, position = "Not Provided", "Not Provided"
                # platenumber, position = getPlateNumberAndPosition(file_name)

                file_type = file["type"]
                file_download_url = file["download_link"]
                if file_download_url == None or file_download_url == "":
                    file_download_url = "Closed Access"
                associated_data_csv.append(
                    {
                        "Station": station,
                        "Country": country,
                        "ARMS_unit": ARMS_unit,
                        "date_start": date_start,
                        "date_end": date_end,
                        "Event_id": event_description,
                        "File_Name": file_name,
                        "File_Type": file_type,
                        "Plate_Number": platenumber,
                        "Position": position,
                        "File_Download_URL": file_download_url,
                        "created_at": created,
                        "updated_at": updated,
                    }
                )
                associated_csv_data.append(
                    {
                        "Station": station,
                        "Country": country,
                        "ARMS_unit": ARMS_unit,
                        "date_start": date_start,
                        "date_end": date_end,
                        "Event_id": event_description,
                        "File_Name": file_name,
                        "Plate_Number": platenumber,
                        "Position": position,
                        "File_Type": file_type,
                        "File_Download_URL": file_download_url,
                        "created_at": created,
                        "updated_at": updated,
                    }
                )

            main_csv_data.append(
                {
                    "Station": station,
                    "Country": country,
                    "ARMS_unit": ARMS_unit,
                    "Latitude": latitude,
                    "Longitude": longitude,
                    "Depth_min": depth_min,
                    "Depth_max": depth_max,
                    "Date_start": date_start,
                    "Date_end": date_end,
                    "Event_ID": event_description,
                    "Material Samples": material_samples,
                    "Observations": observations,
                    "Sequences": sequences,
                    "Associated Data": associated_date,
                    "Created": created,
                    "Updated": updated,
                }
            )

            main_data_csv.append(
                {
                    "Station": station,
                    "Country": country,
                    "ARMS_unit": ARMS_unit,
                    "Latitude": latitude,
                    "Longitude": longitude,
                    "Depth_min": depth_min,
                    "Depth_max": depth_max,
                    "Date_start": date_start,
                    "Date_end": date_end,
                    "Event_ID": event_description,
                    "Event_Description": description,
                    "IUCN_Habitat_type": iucn_habitat_type,
                    "Material Samples": material_samples,
                    "Observations": observations,
                    "Sequences": sequences,
                    "Associated Data": associated_date,
                    "Created": created,
                    "Updated": updated,
                }
            )

    with open(
        os.path.join(
            output_dir, ew_sampling_area_name, "material_samples_" + station + ".csv"
        ),
        "w",
        newline="",
    ) as csvfile:
        fieldnames = [
            "Material_Sample_ID",
            "Parent_Event_ID",
            "Description",
            "Created_At",
            "Updated_At",
            "Sequences",
            "Associated data",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in material_samples_csv:
            writer.writerow(data)

    with open(
        os.path.join(
            output_dir, ew_sampling_area_name, "observations_" + station + ".csv"
        ),
        "w",
        newline="",
    ) as csvfile:
        fieldnames = [
            "Station",
            "Country",
            "ARMS_unit",
            "date_start",
            "date_end",
            "Event_id",
            "Remarks",
            "Is_Varified",
            "Taxon_Name",
            "created_at",
            "updated_at",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in observations_csv:
            writer.writerow(data)

    with open(
        os.path.join(
            output_dir, ew_sampling_area_name, "sequences_" + station + ".csv"
        ),
        "w",
        newline="",
    ) as csvfile:
        fieldnames = [
            "Station",
            "Country",
            "ARMS_unit",
            "date_start",
            "date_end",
            "Event_id",
            "Sequence_ID",
            "Sequence",
            "Chimeric",
            "Unite_Status",
            "Low_Quality",
            "Forward_Primer",
            "Reverse_Primer",
            "Remarks",
            "Regions",
            "created_at",
            "updated_at",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in sequences_csv:
            writer.writerow(data)

    with open(
        os.path.join(
            output_dir, ew_sampling_area_name, "associated_data_" + station + ".csv"
        ),
        "w",
        newline="",
    ) as csvfile:
        fieldnames = [
            "Station",
            "Country",
            "ARMS_unit",
            "date_start",
            "date_end",
            "Event_id",
            "File_Name",
            "Plate_Number",
            "Position",
            "File_Type",
            "File_Download_URL",
            "created_at",
            "updated_at",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in associated_data_csv:
            # decode all the binary values in the data dict by utf-8 and encode them to cp850 and then decode again by cp580
            #
            data = {
                k: v.encode("cp850", "replace").decode("cp850") for k, v in data.items()
            }
            writer.writerow(data)

    with open(
        os.path.join(
            output_dir, ew_sampling_area_name, "overview_data_" + station + ".csv"
        ),
        "w",
        newline="",
    ) as csvfile:
        fieldnames = [
            "Station",
            "Country",
            "ARMS_unit",
            "Latitude",
            "Longitude",
            "Depth_min",
            "Depth_max",
            "Date_start",
            "Date_end",
            "Event_ID",
            "Event_Description",
            "IUCN_Habitat_type",
            "Material Samples",
            "Observations",
            "Sequences",
            "Associated Data",
            "Created",
            "Updated",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in main_data_csv:
            data = {
                k: str(v).encode("cp850", "replace").decode("cp850")
                for k, v in data.items()
            }
            writer.writerow(data)

# write the main.csv
with open(os.path.join(output_dir, "AllOverview.csv"), "w", newline="") as csvfile:
    fieldnames = [
        "Station",
        "Country",
        "ARMS_unit",
        "Latitude",
        "Longitude",
        "Depth_min",
        "Depth_max",
        "Date_start",
        "Date_end",
        "Event_ID",
        "Material Samples",
        "Observations",
        "Sequences",
        "Associated Data",
        "Created",
        "Updated",
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in main_csv_data:
        writer.writerow(data)

# write the associated.csv
with open(
    os.path.join(output_dir, "AllAssociatedData.csv"), "w", newline=""
) as csvfile:
    fieldnames = [
        "Station",
        "Country",
        "ARMS_unit",
        "date_start",
        "date_end",
        "Event_id",
        "File_Name",
        "Plate_Number",
        "Position",
        "File_Type",
        "File_Download_URL",
        "created_at",
        "updated_at",
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in associated_csv_data:
        data = {
            k: v.encode("cp850", "replace").decode("cp850") for k, v in data.items()
        }
        writer.writerow(data)

# write the sequences.csv
with open(os.path.join(output_dir, "AllSequences.csv"), "w", newline="") as csvfile:
    fieldnames = [
        "Station",
        "Country",
        "ARMS_unit",
        "date_start",
        "date_end",
        "Event_id",
        "Sequence_ID",
        "Sequence",
        "Chimeric",
        "Unite_Status",
        "Low_Quality",
        "Forward_Primer",
        "Reverse_Primer",
        "Remarks",
        "Regions",
        "created_at",
        "updated_at",
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in sequences_csv_data:
        writer.writerow(data)

# write the observations.csv
with open(os.path.join(output_dir, "AllObservations.csv"), "w", newline="") as csvfile:
    fieldnames = [
        "Station",
        "Country",
        "ARMS_unit",
        "date_start",
        "date_end",
        "Event_id",
        "Remarks",
        "Is_Varified",
        "Taxon_Name",
        "created_at",
        "updated_at",
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in observations_csv_data:
        writer.writerow(data)

# write the material_samples.csv
with open(
    os.path.join(output_dir, "AllMaterialSamples.csv"), "w", newline=""
) as csvfile:
    fieldnames = [
        "Material_Sample_ID",
        "Parent_Event_ID",
        "Description",
        "Created_At",
        "Updated_At",
        "Sequences",
        "Associated data",
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in material_samples_csv_data:
        writer.writerow(data)

filename = "PlutoF_HarvestQCreport.csv"  # In same directory as script

# make csv file from csv_file_QC_output
with open(os.path.join(output_dir, filename), "w", newline="") as csvfile:
    fieldnames = ["station", "country", "unit", "qc_param", "qc_flag"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in csv_file_QC_output:
        writer.writerow(data)

# perform a download of a google sheet and import each sheet as a json file : url = https://docs.google.com/spreadsheets/d/1j3yuY5lmoPMo91w6e3kkJ6pmp1X6FVGUtLealuKJ3wE/edit#gid=1607535453
url = "https://docs.google.com/spreadsheets/d/1j3yuY5lmoPMo91w6e3kkJ6pmp1X6FVGUtLealuKJ3wE/export?format=csv&id=1j3yuY5lmoPMo91w6e3kkJ6pmp1X6FVGUtLealuKJ3wE&gid=1607535453"
r = requests.get(url, allow_redirects=True)
print(r.status_code)
with open(os.path.join(output_dir, "GS_ARMS_Observatory.csv"), "wb") as f:
    f.write(r.content)

# same for the arms_samples_sequences
url = "https://docs.google.com/spreadsheets/d/1j3yuY5lmoPMo91w6e3kkJ6pmp1X6FVGUtLealuKJ3wE/export?format=csv&id=1j3yuY5lmoPMo91w6e3kkJ6pmp1X6FVGUtLealuKJ3wE&gid=855411053"
r = requests.get(url, allow_redirects=True)
with open(os.path.join(output_dir, "GS_ARMS_MaterialSamples_Sequences.csv"), "wb") as f:
    f.write(r.content)

# same for the arms observatory metadata
url = "https://docs.google.com/spreadsheets/d/1j3yuY5lmoPMo91w6e3kkJ6pmp1X6FVGUtLealuKJ3wE/export?format=csv&id=1j3yuY5lmoPMo91w6e3kkJ6pmp1X6FVGUtLealuKJ3wE&gid=2133798758"
r = requests.get(url, allow_redirects=True)
with open(os.path.join(output_dir, "GS_ARMS_Observatory_Metadata.csv"), "wb") as f:
    f.write(r.content)

# same for the arms material_samples and sequence info metadata
url = "https://docs.google.com/spreadsheets/d/1j3yuY5lmoPMo91w6e3kkJ6pmp1X6FVGUtLealuKJ3wE/export?format=csv&id=1j3yuY5lmoPMo91w6e3kkJ6pmp1X6FVGUtLealuKJ3wE&gid=1582985605"
r = requests.get(url, allow_redirects=True)
with open(
    os.path.join(output_dir, "GS_ARMS_MaterialSamples_Sequence_Metadata.csv"), "wb"
) as f:
    f.write(r.content)

# make a QC report for the ARMS Observatory info comparing data from AllObservations.csv and ARMS_Observatory_info.csv
qc_report_arms_observatories_plutoF_to_gsheets = []
qc_report_arms_observatories_gsheets_to_plutoF = []
qc_observatory_info = []


# load in Arms Observatory info as json file
def csv_to_json(csv_file_path):
    # create a dictionary
    data_dict = []
    # Step 2
    # open a csv file handler
    with open(csv_file_path, encoding="utf-8") as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)
        # convert each row into a dictionary
        # and add the converted data to the data_variable
        for rows in csv_reader:
            data_dict.append(rows)
    return data_dict


json_arms_observatories_gsheets = csv_to_json(
    os.path.join(output_dir, "GS_ARMS_Observatory.csv")
)
json_arms_observatories_plutoF = main_csv_data
# a mapping will be placed here in the future where all the culumbs are described that should be compared

# begin the plutoF to gsheets QC
for plutoF_data in json_arms_observatories_plutoF:
    found_observatory = False
    found_arms_id = False
    for gsheets_data in json_arms_observatories_gsheets:
        # check if the observatory name is the same
        try:
            if plutoF_data["Station"] == gsheets_data["Observatory-ID (corrected)"]:
                found_observatory = True
            # check if the arms_id is the same
            if plutoF_data["ARMS_unit"] == gsheets_data["ARMS-ID (corrected)"]:
                found_arms_id = True
            if found_arms_id == True and found_observatory == True:
                pass
        except:
            print("error")
    if found_arms_id == False:
        qc_observatory_info.append(
            {
                "ARMS_unit": plutoF_data["ARMS_unit"],
                "Station": plutoF_data["Station"],
                "QC_comment": "ARMS ID not found in GS",
                "QC_param": "ARMS_ID",
                "QC_value_plutoF": plutoF_data["ARMS_unit"],
                "QC_value_gsheets": "",
            }
        )
    if found_observatory == False:
        qc_observatory_info.append(
            {
                "ARMS_unit": plutoF_data["ARMS_unit"],
                "Station": plutoF_data["Station"],
                "QC_comment": "Observatory not found in GS",
                "QC_param": "Observatory",
                "QC_value_plutoF": plutoF_data["Station"],
                "QC_value_gsheets": "",
            }
        )


# same for gsheets to plutoF
for gsheets_data in json_arms_observatories_gsheets:
    found_observatory = False
    found_arms_id = False
    for plutoF_data in json_arms_observatories_plutoF:
        try:
            # check if the observatory name is the same
            if plutoF_data["Station"] == gsheets_data["Observatory-ID (corrected)"]:
                found_observatory = True

            # check if the arms_id is the same
            if plutoF_data["ARMS_unit"] == gsheets_data["ARMS-ID (corrected)"]:
                found_arms_id = True

            if found_arms_id == True and found_observatory == True:
                if abs(
                    abs(float(plutoF_data["Latitude"]))
                    - abs(float(gsheets_data["Latitude"]))
                ) > (0) or abs(
                    float(plutoF_data["Longitude"]) - float(gsheets_data["Longitude"])
                ) > (
                    0
                ):
                    if abs(
                        abs(float(plutoF_data["Latitude"]))
                        - abs(float(gsheets_data["Latitude"]))
                    ) > (1 / 111.6) or abs(
                        float(plutoF_data["Longitude"])
                        - float(gsheets_data["Longitude"])
                    ) > (
                        1 / 111.6
                    ):
                        qc_observatory_info.append(
                            {
                                "ARMS_unit": gsheets_data["ARMS-ID (corrected)"],
                                "Station": gsheets_data["Country ISO3letter code"],
                                "QC_comment": "Observatory and ARMS ID found but lat or long are SIGNIFICANTLY different",
                                "QC_param": "Lat_Long",
                                "QC_value_plutoF": plutoF_data["Latitude"]
                                + " "
                                + plutoF_data["Longitude"],
                                "QC_value_gsheets": gsheets_data["Latitude"]
                                + " "
                                + gsheets_data["Longitude"],
                            }
                        )
                    else:
                        qc_observatory_info.append(
                            {
                                "ARMS_unit": gsheets_data["ARMS-ID (corrected)"],
                                "Station": gsheets_data["Country ISO3letter code"],
                                "QC_comment": "Observatory and ARMS ID found but lat and long are different",
                                "QC_param": "Lat_Long",
                                "QC_value_plutoF": plutoF_data["Latitude"]
                                + " "
                                + plutoF_data["Longitude"],
                                "QC_value_gsheets": gsheets_data["Latitude"]
                                + " "
                                + gsheets_data["Longitude"],
                            }
                        )
                else:
                    qc_observatory_info.append(
                        {
                            "ARMS_unit": gsheets_data["ARMS-ID (corrected)"],
                            "Station": gsheets_data["Country ISO3letter code"],
                            "QC_comment": "OK",
                        }
                    )
                break
        except:
            pass
    if found_arms_id == False:
        qc_observatory_info.append(
            {
                "ARMS_unit": gsheets_data["ARMS-ID (corrected)"],
                "Station": gsheets_data["Country ISO3letter code"],
                "QC_comment": "ARMS ID not found in PlutoF",
                "QC_param": "ARMS_ID",
                "QC_value_plutoF": "",
                "QC_value_gsheets": gsheets_data["ARMS-ID (corrected)"],
            }
        )
    if found_observatory == False:
        qc_observatory_info.append(
            {
                "ARMS_unit": gsheets_data["ARMS-ID (corrected)"],
                "Station": gsheets_data["Country ISO3letter code"],
                "QC_comment": "Observatory not found in PlutoF",
                "QC_param": "Observatory",
                "QC_value_plutoF": "",
                "QC_value_gsheets": gsheets_data["Country ISO3letter code"],
            }
        )


# begin the plutoF to gsheets QC
for plutoF_data in json_arms_observatories_plutoF:
    found = False
    for gsheets_data in json_arms_observatories_gsheets:
        # begin with the rules
        # if the arms_id is the same then begin checking the rules
        if plutoF_data["ARMS_unit"] == gsheets_data["ARMS-ID (corrected)"]:
            found = True
            # go over the rules
            # check if the lat; long and depth are the same
            try:
                if float(plutoF_data["Latitude"]) != float(gsheets_data["Latitude"]):
                    # check if the difference is less than 2m and if so then pass
                    if abs(
                        abs(float(plutoF_data["Latitude"]))
                        - abs(float(gsheets_data["Latitude"]))
                    ) > (1 / 111.6):
                        qc_report_arms_observatories_plutoF_to_gsheets.append(
                            {
                                "station": plutoF_data["Station"],
                                "arms_unit": plutoF_data["ARMS_unit"],
                                "qc_param": "latitude",
                                "qc_flag": "fail",
                                "plutoF_data": plutoF_data["Latitude"],
                                "gsheets_data": gsheets_data["Latitude"],
                            }
                        )
                    else:
                        qc_report_arms_observatories_plutoF_to_gsheets.append(
                            {
                                "station": plutoF_data["Station"],
                                "arms_unit": plutoF_data["ARMS_unit"],
                                "qc_param": "latitude",
                                "qc_flag": "value is different but not significantly",
                                "plutoF_data": plutoF_data["Latitude"],
                                "gsheets_data": gsheets_data["Latitude"],
                            }
                        )
            except:
                qc_report_arms_observatories_plutoF_to_gsheets.append(
                    {
                        "station": plutoF_data["Station"],
                        "arms_unit": plutoF_data["ARMS_unit"],
                        "qc_param": "latitude",
                        "qc_flag": "fail",
                        "plutoF_data": plutoF_data["Latitude"],
                        "gsheets_data": gsheets_data["Latitude"],
                    }
                )

            try:
                if float(plutoF_data["Longitude"]) != float(gsheets_data["Longitude"]):
                    if abs(
                        abs(float(plutoF_data["Longitude"]))
                        - abs(float(gsheets_data["Longitude"]))
                    ) > (1 / 111.6):
                        qc_report_arms_observatories_plutoF_to_gsheets.append(
                            {
                                "station": plutoF_data["Station"],
                                "arms_unit": plutoF_data["ARMS_unit"],
                                "qc_param": "longitude",
                                "qc_flag": "fail",
                                "plutoF_data": plutoF_data["Longitude"],
                                "gsheets_data": gsheets_data["Longitude"],
                            }
                        )
                    else:
                        qc_report_arms_observatories_plutoF_to_gsheets.append(
                            {
                                "station": plutoF_data["Station"],
                                "arms_unit": plutoF_data["ARMS_unit"],
                                "qc_param": "longitude",
                                "qc_flag": "value is different but not significantly",
                                "plutoF_data": plutoF_data["Longitude"],
                                "gsheets_data": gsheets_data["Longitude"],
                            }
                        )
            except:
                qc_report_arms_observatories_plutoF_to_gsheets.append(
                    {
                        "station": plutoF_data["Station"],
                        "arms_unit": plutoF_data["ARMS_unit"],
                        "qc_param": "longitude",
                        "qc_flag": "fail",
                        "plutoF_data": plutoF_data["Longitude"],
                        "gsheets_data": gsheets_data["Longitude"],
                    }
                )

            try:
                if float(plutoF_data["Depth_min"]) != float(
                    gsheets_data["Depth_min (m)"]
                ):
                    if (
                        abs(
                            float(plutoF_data["Depth_min"])
                            - float(gsheets_data["Depth_min (m)"])
                        )
                        > 1
                    ):
                        qc_report_arms_observatories_plutoF_to_gsheets.append(
                            {
                                "station": plutoF_data["Station"],
                                "arms_unit": plutoF_data["ARMS_unit"],
                                "qc_param": "depth",
                                "qc_flag": "fail",
                                "plutoF_data": plutoF_data["Depth_min"],
                                "gsheets_data": gsheets_data["Depth_min (m)"],
                            }
                        )
            except:
                qc_report_arms_observatories_plutoF_to_gsheets.append(
                    {
                        "station": plutoF_data["Station"],
                        "arms_unit": plutoF_data["ARMS_unit"],
                        "qc_param": "depth",
                        "qc_flag": "fail",
                        "plutoF_data": plutoF_data["Depth_min"],
                        "gsheets_data": gsheets_data["Depth_min (m)"],
                    }
                )

            try:
                if (
                    float(plutoF_data["Latitude"]) == float(gsheets_data["Latitude"])
                    and float(plutoF_data["Longitude"])
                    == float(gsheets_data["Longitude"])
                    and float(plutoF_data["Depth_min"])
                    == float(gsheets_data["Depth_min (m)"])
                ):
                    qc_report_arms_observatories_plutoF_to_gsheets.append(
                        {
                            "station": plutoF_data["Station"],
                            "arms_unit": plutoF_data["ARMS_unit"],
                            "qc_param": "latitude, longitude, depth",
                            "qc_flag": "pass",
                        }
                    )
            except:
                qc_report_arms_observatories_plutoF_to_gsheets.append(
                    {
                        "station": plutoF_data["Station"],
                        "arms_unit": plutoF_data["ARMS_unit"],
                        "qc_param": "latitude, longitude, depth",
                        "qc_flag": "pass",
                    }
                )
    if found == False:
        qc_report_arms_observatories_plutoF_to_gsheets.append(
            {
                "station": plutoF_data["Station"],
                "arms_unit": plutoF_data["ARMS_unit"],
                "qc_param": "arms_unit",
                "qc_flag": "fail",
                "plutoF_data": plutoF_data["ARMS_unit"],
                "gsheets_data": gsheets_data["ARMS-ID (corrected)"],
            }
        )

# do the same for the gsheets to plutoF QC
for gsheets_data in json_arms_observatories_gsheets:
    found = False
    for plutoF_data in json_arms_observatories_plutoF:
        if gsheets_data["ARMS-ID (corrected)"] == plutoF_data["ARMS_unit"]:
            found = True
            # go over the rules
            try:
                if float(gsheets_data["Latitude"]) != float(plutoF_data["Latitude"]):
                    # if the first 2 characters after the . are the same then pass
                    if abs(
                        abs(float(gsheets_data["Latitude"]))
                        - abs(float(plutoF_data["Latitude"]))
                    ) > (1 / 111.6):
                        qc_report_arms_observatories_gsheets_to_plutoF.append(
                            {
                                "station": gsheets_data["Observatory-ID (corrected)"],
                                "arms_id": gsheets_data["ARMS-ID (corrected)"],
                                "qc_param": "latitude",
                                "qc_flag": "fail",
                                "gsheets_data": gsheets_data["Latitude"],
                                "plutoF_data": plutoF_data["Latitude"],
                            }
                        )
                    else:
                        qc_report_arms_observatories_gsheets_to_plutoF.append(
                            {
                                "station": gsheets_data["Observatory-ID (corrected)"],
                                "arms_id": gsheets_data["ARMS-ID (corrected)"],
                                "qc_param": "latitude",
                                "qc_flag": "value is different but not significantly",
                                "gsheets_data": gsheets_data["Latitude"],
                                "plutoF_data": plutoF_data["Latitude"],
                            }
                        )
            except:
                qc_report_arms_observatories_gsheets_to_plutoF.append(
                    {
                        "station": gsheets_data["Observatory-ID (corrected)"],
                        "arms_id": gsheets_data["ARMS-ID (corrected)"],
                        "qc_param": "latitude",
                        "qc_flag": "fail",
                        "gsheets_data": gsheets_data["Latitude"],
                        "plutoF_data": plutoF_data["Latitude"],
                    }
                )
            try:
                if float(gsheets_data["Longitude"]) != float(plutoF_data["Longitude"]):
                    if abs(
                        abs(float(gsheets_data["Longitude"]))
                        - abs(float(plutoF_data["Longitude"]))
                    ) > (1 / 111.6):
                        qc_report_arms_observatories_gsheets_to_plutoF.append(
                            {
                                "station": gsheets_data["Observatory-ID (corrected)"],
                                "arms_id": gsheets_data["ARMS-ID (corrected)"],
                                "qc_param": "longitude",
                                "qc_flag": "fail",
                                "gsheets_data": gsheets_data["Longitude"],
                                "plutoF_data": plutoF_data["Longitude"],
                            }
                        )
                    else:
                        qc_report_arms_observatories_gsheets_to_plutoF.append(
                            {
                                "station": gsheets_data["Observatory-ID (corrected)"],
                                "arms_id": gsheets_data["ARMS-ID (corrected)"],
                                "qc_param": "longitude",
                                "qc_flag": "value is different but not significantly",
                                "gsheets_data": gsheets_data["Longitude"],
                                "plutoF_data": plutoF_data["Longitude"],
                            }
                        )
            except:
                qc_report_arms_observatories_gsheets_to_plutoF.append(
                    {
                        "station": gsheets_data["Observatory-ID (corrected)"],
                        "arms_id": gsheets_data["ARMS-ID (corrected)"],
                        "qc_param": "longitude",
                        "qc_flag": "fail",
                        "gsheets_data": gsheets_data["Longitude"],
                        "plutoF_data": plutoF_data["Longitude"],
                    }
                )
            try:
                if float(gsheets_data["Depth_min (m)"]) != float(
                    plutoF_data["Depth_min"]
                ):
                    if (
                        abs(
                            float(gsheets_data["Depth_min (m)"])
                            - float(plutoF_data["Depth_min"])
                        )
                        > 1
                    ):
                        qc_report_arms_observatories_gsheets_to_plutoF.append(
                            {
                                "station": gsheets_data["Observatory-ID (corrected)"],
                                "arms_id": gsheets_data["ARMS-ID (corrected)"],
                                "qc_param": "depth",
                                "qc_flag": "fail",
                                "gsheets_data": gsheets_data["Depth_min (m)"],
                                "plutoF_data": plutoF_data["Depth_min"],
                            }
                        )
            except:
                qc_report_arms_observatories_gsheets_to_plutoF.append(
                    {
                        "station": gsheets_data["Observatory-ID (corrected)"],
                        "arms_id": gsheets_data["ARMS-ID (corrected)"],
                        "qc_param": "depth",
                        "qc_flag": "fail",
                        "gsheets_data": gsheets_data["Depth_min (m)"],
                        "plutoF_data": plutoF_data["Depth_min"],
                    }
                )
            try:
                if (
                    float(gsheets_data["Latitude"]) == float(plutoF_data["Latitude"])
                    and float(gsheets_data["Longitude"])
                    == float(plutoF_data["Longitude"])
                    and float(gsheets_data["Depth_min (m)"])
                    == float(plutoF_data["Depth_min"])
                ):
                    qc_report_arms_observatories_gsheets_to_plutoF.append(
                        {
                            "station": gsheets_data["Observatory-ID (corrected)"],
                            "arms_id": gsheets_data["ARMS-ID (corrected)"],
                            "qc_param": "latitude, longitude, depth",
                            "qc_flag": "pass",
                        }
                    )
            except:
                qc_report_arms_observatories_gsheets_to_plutoF.append(
                    {
                        "station": gsheets_data["Observatory-ID (corrected)"],
                        "arms_id": gsheets_data["ARMS-ID (corrected)"],
                        "qc_param": "latitude, longitude, depth",
                        "qc_flag": "pass",
                    }
                )
    if found == False:
        qc_report_arms_observatories_gsheets_to_plutoF.append(
            {
                "station": gsheets_data["Observatory-ID (corrected)"],
                "arms_id": gsheets_data["ARMS-ID (corrected)"],
                "qc_param": "arms_id",
                "qc_flag": "fail",
                "gsheets_data": gsheets_data["ARMS-ID (corrected)"],
                "plutoF_data": plutoF_data["ARMS_unit"],
            }
        )

# write away the reports to a csv file
with open(
    os.path.join(output_dir, "qc_report_arms_observatories_plutoF_to_gsheets.csv"),
    "w",
    newline="",
) as f:
    fieldnames = [
        "station",
        "arms_unit",
        "qc_param",
        "qc_flag",
        "plutoF_data",
        "gsheets_data",
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for data in qc_report_arms_observatories_plutoF_to_gsheets:
        writer.writerow(data)

with open(
    os.path.join(output_dir, "qc_report_arms_observatories_gsheets_to_plutoF.csv"),
    "w",
    newline="",
) as f:
    fieldnames = [
        "station",
        "arms_id",
        "qc_param",
        "qc_flag",
        "gsheets_data",
        "plutoF_data",
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for data in qc_report_arms_observatories_gsheets_to_plutoF:
        writer.writerow(data)

with open(
    os.path.join(output_dir, "qc_report_observatory_info.csv"), "w", newline=""
) as f:
    fieldnames = [
        "ARMS_unit",
        "Station",
        "QC_comment",
        "QC_param",
        "QC_value_plutoF",
        "QC_value_gsheets",
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for data in qc_observatory_info:
        writer.writerow(data)


# perform the same qc for the samples
qc_report_arms_samples_plutoF_to_gsheets = []
qc_report_arms_samples_gsheets_to_plutoF = []

json_arms_samples_gsheets = csv_to_json(
    os.path.join(output_dir, "GS_ARMS_MaterialSamples_Sequences.csv")
)
json_arms_samples_plutoF = material_samples_csv_data
print(material_samples_csv_data)

# begin the plutoF to gsheets QC
for plutoF_data in json_arms_samples_plutoF:
    found = False
    # print(plutoF_data)
    for gsheets_data in json_arms_samples_gsheets:
        if plutoF_data["Parent_Event_ID"] == gsheets_data["Event-ID"]:
            found = True

    if found == False:
        qc_report_arms_samples_plutoF_to_gsheets.append(
            {
                "sample": plutoF_data["Material_Sample_ID"],
                "qc_param": "event_id",
                "qc_flag": "fail",
                "plutoF_data": plutoF_data["Parent_Event_ID"],
                "gsheets_data": "not found",
            }
        )
    if found == True:
        sample_found = False
        for gsheets_data in json_arms_samples_gsheets:
            if plutoF_data["Material_Sample_ID"] == gsheets_data["MaterialSample-ID"]:
                sample_found = True
        if sample_found == False:
            qc_report_arms_samples_plutoF_to_gsheets.append(
                {
                    "sample": plutoF_data["Material_Sample_ID"],
                    "qc_param": "sample_id",
                    "qc_flag": "fail",
                    "plutoF_data": plutoF_data["Material_Sample_ID"],
                    "gsheets_data": "not found",
                }
            )

        if sample_found == True:
            qc_report_arms_samples_plutoF_to_gsheets.append(
                {
                    "sample": plutoF_data["Material_Sample_ID"],
                    "qc_param": "sample_id",
                    "qc_flag": "pass",
                }
            )

# do the same for gsheets to plutoF
for gsheets_data in json_arms_samples_gsheets:
    found = False
    for plutof_data in json_arms_samples_plutoF:
        # first check if the event id is the same
        if gsheets_data["Event-ID"] == plutof_data["Parent_Event_ID"]:
            found = True

    if found == False:
        qc_report_arms_observatories_gsheets_to_plutoF.append(
            {
                "sample": gsheets_data["MaterialSample-ID"],
                "qc_param": "event_id",
                "qc_flag": "fail",
                "plutoF_data": "not found",
                "gsheets_data": gsheets_data["Event-ID"],
            }
        )

    if found == True:
        sample_found = False
        for plutof_data in json_arms_samples_plutoF:
            if gsheets_data["MaterialSample-ID"] == plutof_data["Material_Sample_ID"]:
                sample_found = True
        if sample_found == False:
            qc_report_arms_samples_gsheets_to_plutoF.append(
                {
                    "sample": gsheets_data["MaterialSample-ID"],
                    "qc_param": "sample_id",
                    "qc_flag": "fail",
                    "plutoF_data": "not found",
                    "gsheets_data": gsheets_data["MaterialSample-ID"],
                }
            )
        if sample_found == True:
            qc_report_arms_samples_gsheets_to_plutoF.append(
                {
                    "sample": gsheets_data["MaterialSample-ID"],
                    "qc_param": "sample_id",
                    "qc_flag": "pass",
                }
            )

# make a qc report that will compare the events in plutoF to the events in gsheets
# the file will be called qc_report_events.csv
# The CSV can have columns: Event-ID from GS, Deployment Date from GS, Collection Date from GS, Event_id from PlutoF, Date_start from PlutoF, Date_end from PlutoF.
# if there is no PlutoF event for a GS, then the cell value under "Event_id from PlutoF" is "missing" and the date cell values can be blank/"missing".
# If there is no GS event for a Plutof, then the cell value under"Event-ID from GS" is "missing" and the date cell values can be blank/"missing".
# Note that while the date part of the Event-ID should be the same as the deployment and collection date values,
# there is no guarantee that this will be so: hence we treat the EventID as the key as the dates as values
# that I will manually compare to the date part of the EventID. So please do stick to the YYYY-MM-DD format.
qc_events = []

# from plutoF to gsheets
for plutoF_data in main_csv_data:
    found = False
    for gs_data in json_arms_samples_gsheets:
        # check if the event id is the same
        if plutoF_data["Event_ID"] == gs_data["Event-ID"]:
            qc_events.append(
                {
                    "Event-ID from GS": gs_data["Event-ID"],
                    "Deployment Date from GS": gs_data["Deployment Date"],
                    "Collection Date from GS": gs_data["Collection Date"],
                    "Event_id from PlutoF": plutoF_data["Event_ID"],
                    "Date_start from PlutoF": plutoF_data["Date_start"],
                    "Date_end from PlutoF": plutoF_data["Date_end"],
                }
            )
            found = True
            break
    if found == False:
        qc_events.append(
            {
                "Event-ID from GS": "missing",
                "Deployment Date from GS": "missing",
                "Collection Date from GS": "missing",
                "Event_id from PlutoF": plutoF_data["Event_ID"],
                "Date_start from PlutoF": plutoF_data["Date_start"],
                "Date_end from PlutoF": plutoF_data["Date_end"],
            }
        )

# from gsheets to plutoF
for gs_data in json_arms_samples_gsheets:
    found = False
    for plutoF_data in main_csv_data:
        if gs_data["Event-ID"] == plutoF_data["Event_ID"]:
            found = True
            present = False
            # check if the event id already in the list
            if len(qc_events) > 0:
                for qc_event in qc_events:
                    if qc_event["Event-ID from GS"] == gs_data["Event-ID"]:
                        present = True
                        break
            if present == False:
                qc_events.append(
                    {
                        "Event-ID from GS": gs_data["Event-ID"],
                        "Deployment Date from GS": gs_data["Deployment Date"],
                        "Collection Date from GS": gs_data["Collection Date"],
                        "Event_id from PlutoF": plutoF_data["Event_ID"],
                        "Date_start from PlutoF": plutoF_data["Date_start"],
                        "Date_end from PlutoF": plutoF_data["Date_end"],
                    }
                )
            break
    if found == False:
        qc_events.append(
            {
                "Event-ID from GS": gs_data["Event-ID"],
                "Deployment Date from GS": gs_data["Deployment Date"],
                "Collection Date from GS": gs_data["Collection Date"],
                "Event_id from PlutoF": "missing",
                "Date_start from PlutoF": "missing",
                "Date_end from PlutoF": "missing",
            }
        )

# write the qc report to csv
with open(
    os.path.join(output_dir, "qc_report_events.csv"), "w", newline="", encoding="utf-8"
) as csvfile:
    fieldnames = [
        "Event-ID from GS",
        "Deployment Date from GS",
        "Collection Date from GS",
        "Event_id from PlutoF",
        "Date_start from PlutoF",
        "Date_end from PlutoF",
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in qc_events:
        writer.writerow(row)

# write both reports to csv
with open(
    os.path.join(output_dir, "qc_report_arms_samples_plutoF_to_gsheets.csv"),
    "w",
    newline="",
    encoding="utf-8",
) as csvfile:
    fieldnames = ["sample", "qc_param", "qc_flag", "plutoF_data", "gsheets_data"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in qc_report_arms_samples_plutoF_to_gsheets:
        writer.writerow(row)

with open(
    os.path.join(output_dir, "qc_report_arms_samples_gsheets_to_plutoF.csv"),
    "w",
    newline="",
    encoding="utf-8",
) as csvfile:
    fieldnames = ["sample", "qc_param", "qc_flag", "plutoF_data", "gsheets_data"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in qc_report_arms_samples_gsheets_to_plutoF:
        writer.writerow(row)

# cut all the files that start with GS_ARMS_ and end with .csv and put them in the parent folder of the output folder /from_gs
for file in os.listdir(output_dir):
    if file.startswith("GS_ARMS_") and file.endswith(".csv"):
        # make the string of the file path to move
        # split the output_dir string on the os sep and pop the last element and rejoin the string by os.sep
        parent_folder = os.sep.join(output_dir.split(os.sep)[:-1])
        shutil.move(
            os.path.join(output_dir, file), os.path.join(parent_folder, "from_gs", file)
        )

# do the same for all the files that start with qc_report
for file in os.listdir(output_dir):
    if file.startswith("qc_report"):
        # make the string of the file path to move
        # split the output_dir string on the os sep and pop the last element and rejoin the string by os.sep
        parent_folder = os.sep.join(output_dir.split(os.sep)[:-1])
        shutil.move(
            os.path.join(output_dir, file), os.path.join(parent_folder, "from_gs", file)
        )

# combine gsheets data with plutoF data in one file
SamplingEventData = []
NonMatchingSamplingEventData = []
ObservatoryData = []
OmicsData = []
ImageData = []

##ObservatoryData
# country from gsheets["Country ISO3letter code"]
# ObservatoryID gsheets["Observatory-ID (corrected)"]
# UnitID gsheets["ARMS-ID (corrected)"]
# Latitude gsheets["Latitude"]
# Longitude gsheets["Longitude"]
# Depth gsheets["Depth_min (m)"]
# fieldReplicate gsheets["fieldReplicate"]
# Monitoring area  gsheets["Monitoring area"]
# Anthropogenic influence gsheets["Anthropogenic influence (env_local)"]
for gsheets_data in json_arms_observatories_gsheets:
    for plutoF_data in main_csv_data:
        if gsheets_data["ARMS-ID (corrected)"] == plutoF_data["ARMS_unit"]:
            ObservatoryData.append(
                {
                    "Country": gsheets_data["Country ISO3letter code"],
                    "ObservatoryID": gsheets_data["Observatory-ID (corrected)"],
                    "UnitID": gsheets_data["ARMS-ID (corrected)"],
                    "Latitude": gsheets_data["Latitude"],
                    "Longitude": gsheets_data["Longitude"],
                    "Depth_min": plutoF_data["Depth_min"],
                    "Depth_max": plutoF_data["Depth_max"],
                    # "fieldReplicate":gsheets_data["fieldReplicate"],
                    "Monitoring area": gsheets_data["Monitoring area"],
                    "Anthropogenic influence": gsheets_data["Anthropogenic influence"],
                    "IUCN habitat type": gsheets_data["IUCN habitat type"],
                    "Description": gsheets_data["Description"],
                    "Notes": gsheets_data["Notes"],
                    "ENVO broad scale": gsheets_data["ENVO_broad_scale"],
                    "ENVO local scale": gsheets_data["ENVO_local_scale"],
                    "ENVO medium scale": gsheets_data["ENVO_medium_scale"],
                    "add info": gsheets_data["add. info"],
                    "MarineRegion_larger": gsheets_data["MarineRegion_larger"],
                    "MarineRegion_smaller": gsheets_data["MarineRegion_smaller"],
                }
            )

##SamplingEventData
# country from gsheets["Country ISO3letter code"]
# ObservatoryID gsheets["Observatory-ID (corrected)"]
# UnitID gsheets["ARMS-ID (corrected)"]
# DateDeployed gsheets["Deployment Date"]
# DateCollected gsheets["Collection Date"]
# Event-ID gsheets["Event-ID"]
# MaterialSampleID gsheets["MaterialSample-ID"]
# Fraction gsheets["Fraction"]
# Preservative gsheets["Preservative"]
# Filter gsheets["Filter (micrometer)"]
# CrateCover gsheets["Crate cover used during retrieval"]
# Number of images => for item in accomsiated data files, if item["Event-ID"] == gsheets["Event-ID"], count += 1

for gsheets_data in json_arms_samples_gsheets:
    count = 0
    for item in associated_csv_data:
        if item["Event_id"] == gsheets_data["Event-ID"]:
            count += 1

    Sequences_available = []
    # if gsheets_data["gene_COI"] =starts with ERR
    if gsheets_data["gene_COI"].startswith("ERR"):
        if "COI" not in Sequences_available:
            Sequences_available.append("COI")
    if gsheets_data["gene_COI_negative_control"].startswith("ERR"):
        pass
    if gsheets_data["gene_ITS"].startswith("ERR"):
        if "ITS" not in Sequences_available:
            Sequences_available.append("ITS")
    if gsheets_data["gene_ITS_negative_control"].startswith("ERR"):
        pass
    if gsheets_data["gene_18S"].startswith("ERR"):
        if "18S" not in Sequences_available:
            Sequences_available.append("18S")
    if gsheets_data["gene_18S_negative_control"].startswith("ERR"):
        pass

    for observatories in ObservatoryData:
        if gsheets_data["Observatory-ID"] == observatories["ObservatoryID"]:
            country = observatories["Country"]

    # check if eventid is in the plutoF data
    for plutoF_data in material_samples_csv_data:
        # print(plutoF_data)
        # print(plutoF_data["Parent_Event_ID"])
        if gsheets_data["Event-ID"] == plutoF_data["Parent_Event_ID"]:
            print("event id in plutoF data :" + gsheets_data["Event-ID"])
            SamplingEventData.append(
                {
                    "Country": country,
                    "ObservatoryID": gsheets_data["Observatory-ID"],
                    "UnitID": gsheets_data["ARMS-ID"],
                    "DateDeployed": gsheets_data["Deployment Date"],
                    "DateCollected": gsheets_data["Collection Date"],
                    "EventID": gsheets_data["Event-ID"],
                    "MaterialSampleID": gsheets_data["MaterialSample-ID"],
                    "FieldReplicate": (
                        gsheets_data["fieldReplicate"]
                        if gsheets_data["fieldReplicate"] != ""
                        else "Not provided"
                    ),
                    "Fraction": (
                        gsheets_data["Fraction"]
                        if gsheets_data["Fraction"] != ""
                        else "Not provided"
                    ),
                    "Preservative": (
                        gsheets_data["Preservative"]
                        if gsheets_data["Preservative"] != ""
                        else "Not provided"
                    ),
                    "SequencingRunRepeat": (
                        gsheets_data["SequencingRunRepeat"]
                        if gsheets_data["SequencingRunRepeat"] != ""
                        else "Not provided"
                    ),
                    "SequencingRunComment": (
                        gsheets_data["SequencingRunComment"]
                        if gsheets_data["SequencingRunComment"] != ""
                        else "Not provided"
                    ),
                    "Filter": (
                        gsheets_data["Filter (micrometer)"]
                        if gsheets_data["Filter (micrometer)"] != ""
                        else "Not provided"
                    ),
                    "CrateCover": (
                        gsheets_data["Crate cover used during retrieval"]
                        if gsheets_data["Crate cover used during retrieval"] != ""
                        else "Not provided"
                    ),
                    "Number of images": str(count),
                    "Sequences available": "; ".join(Sequences_available),
                    "SampleRep": (
                        gsheets_data["SampleRep"]
                        if gsheets_data["SampleRep"] != ""
                        else "Not provided"
                    ),
                    "ReplicateMaterialSampleID": gsheets_data["MaterialSample-ID"],
                }
            )
        else:
            SamplingEventData.append(
                {
                    "Country": country,
                    "ObservatoryID": gsheets_data["Observatory-ID"],
                    "UnitID": gsheets_data["ARMS-ID"],
                    "DateDeployed": gsheets_data["Deployment Date"],
                    "DateCollected": gsheets_data["Collection Date"],
                    "EventID": gsheets_data["Event-ID"],
                    "MaterialSampleID": gsheets_data["MaterialSample-ID"],
                    "FieldReplicate": (
                        gsheets_data["fieldReplicate"]
                        if gsheets_data["fieldReplicate"] != ""
                        else "Not provided"
                    ),
                    "Fraction": (
                        gsheets_data["Fraction"]
                        if gsheets_data["Fraction"] != ""
                        else "Not provided"
                    ),
                    "Preservative": (
                        gsheets_data["Preservative"]
                        if gsheets_data["Preservative"] != ""
                        else "Not provided"
                    ),
                    "SequencingRunRepeat": (
                        gsheets_data["SequencingRunRepeat"]
                        if gsheets_data["SequencingRunRepeat"] != ""
                        else "Not provided"
                    ),
                    "SequencingRunComment": (
                        gsheets_data["SequencingRunComment"]
                        if gsheets_data["SequencingRunComment"] != ""
                        else "Not provided"
                    ),
                    "Filter": (
                        gsheets_data["Filter (micrometer)"]
                        if gsheets_data["Filter (micrometer)"] != ""
                        else "Not provided"
                    ),
                    "CrateCover": (
                        gsheets_data["Crate cover used during retrieval"]
                        if gsheets_data["Crate cover used during retrieval"] != ""
                        else "Not provided"
                    ),
                    "Number of images": str(count),
                    "Sequences available": "; ".join(Sequences_available),
                    "SampleRep": (
                        gsheets_data["SampleRep"]
                        if gsheets_data["SampleRep"] != ""
                        else "Not provided"
                    ),
                    "ReplicateMaterialSampleID": gsheets_data["MaterialSample-ID"],
                }
            )


for plutoF_data in material_samples_csv_data:

    # check if plutoF_data["MaterialSample_ID"] is already part of the SamplingEventData["MaterialSampleID"]
    in_list = False
    for item in SamplingEventData:
        if item["MaterialSampleID"] == plutoF_data["Material_Sample_ID"]:
            in_list = True

    if in_list:
        continue

    for main_data in main_csv_data:
        if plutoF_data["Parent_Event_ID"] == main_data["Event_ID"]:
            country = main_data["Country"]
            Observatory_id = main_data["Station"]
            Unit_id = main_data["ARMS_unit"]

    pre_date_created = plutoF_data["Parent_Event_ID"].split("_")[3]
    date_created = (
        pre_date_created[0:4]
        + "-"
        + pre_date_created[4:6]
        + "-"
        + pre_date_created[6:8]
    )

    pre_date_collected = plutoF_data["Parent_Event_ID"].split("_")[4]
    date_collected = (
        pre_date_collected[0:4]
        + "-"
        + pre_date_collected[4:6]
        + "-"
        + pre_date_collected[6:8]
    )
    try:
        fraction = plutoF_data["Material_Sample_ID"].split("_")[5]
        # seperate fraction from the filter by looking at the string, if the first 2 characters SF => sessile fraction, if MF => motile fraction and then use the remainder as the filter value
        if fraction[0:2] == "SF":
            v_fraction = "sessile fraction"
            v_filter = fraction[2:]
        elif fraction[0:2] == "MF":
            v_filter = fraction[2:]
            v_fraction = "motile fraction"
        else:
            v_fraction = fraction
            v_filter = "Not provided"
    except:
        fraction = ""
    try:
        preservative = plutoF_data["Material_Sample_ID"].split("_")[6]
        # check if preservative is either ETOH or DMSO , if not then it is Not provided
        if preservative == "ETOH" or preservative == "DMSO":
            v_preservative = preservative
        else:
            v_preservative = "Not provided"
    except:
        v_preservative = ""

    SamplingEventData.append(
        {
            "Country": country,
            "ObservatoryID": Observatory_id,
            "UnitID": Unit_id,
            "DateDeployed": date_created,
            "DateCollected": date_collected,
            "EventID": plutoF_data["Parent_Event_ID"],
            "MaterialSampleID": plutoF_data["Material_Sample_ID"],
            "FieldReplicate": "Not provided",
            "Fraction": v_fraction if v_fraction != "" else "Not provided",
            "Preservative": v_preservative if v_preservative != "" else "Not provided",
            "SequencingRunRepeat": "Not provided",
            "SequencingRunComment": "Not provided",
            "Filter": v_filter if v_filter != "" else "Not provided",
            "CrateCover": "Not provided",
            "Number of images": "0",
            "Sequences available": "",
            "SampleRep": "Not provided",
            "ReplicateMaterialSampleID": plutoF_data["Material_Sample_ID"],
        }
    )

for plutoF_data in material_samples_csv_data:
    inGoogleSheets = False
    for obs_plutoF_data in json_arms_observatories_plutoF:
        # get the country from the observatory data by matching the observatory id
        if obs_plutoF_data["Event_ID"] == plutoF_data["Parent_Event_ID"]:
            # get country from the observatory data
            for observatory in ObservatoryData:
                if obs_plutoF_data["Station"] == observatory["ObservatoryID"]:
                    country = observatory["Country"]
            observatoryid = obs_plutoF_data["Station"]
            unitid = obs_plutoF_data["ARMS_unit"]
            date_deployed = obs_plutoF_data["Date_start"]
            collection_date = obs_plutoF_data["Date_end"]
    for gsheets_data in json_arms_samples_gsheets:
        if plutoF_data["Parent_Event_ID"] == gsheets_data["Event-ID"]:
            inGoogleSheets = True
            # check if ENA sequences are available
            Sequences_available = []
            # if gsheets_data["gene_COI"] =starts with ERR
            if gsheets_data["gene_COI"].startswith("ERR"):
                if "COI" not in Sequences_available:
                    Sequences_available.append("COI")
            if gsheets_data["gene_COI_negative_control"].startswith("ERR"):
                pass
            if gsheets_data["gene_ITS"].startswith("ERR"):
                if "ITS" not in Sequences_available:
                    Sequences_available.append("ITS")
            if gsheets_data["gene_ITS_negative_control"].startswith("ERR"):
                pass
            if gsheets_data["gene_18S"].startswith("ERR"):
                if "18S" not in Sequences_available:
                    Sequences_available.append("18S")
            if gsheets_data["gene_18S_negative_control"].startswith("ERR"):
                pass
            print(gsheets_data["Event-ID"] + " is in google sheets")
    if inGoogleSheets == False:
        SamplingEventData.append(
            {
                "Country": country,
                "ObservatoryID": observatoryid,
                "UnitID": unitid,
                "DateDeployed": date_deployed,
                "DateCollected": collection_date,
                "EventID": plutoF_data["Parent_Event_ID"],
                "MaterialSampleID": plutoF_data["Material_Sample_ID"],
                "FieldReplicate": (
                    gsheets_data["fieldReplicate"]
                    if gsheets_data["fieldReplicate"] != ""
                    else "Not provided"
                ),
                "Fraction": gsheets_data["Fraction"],
                "Preservative": "Not provided",
                "SequencingRunRepeat": "Not provided",
                "SequencingRunComment": "Not provided",
                "Filter": "Not provided",
                "CrateCover": "Not provided",
                "Number of images": plutoF_data["Associated data"],
                "Sequences available": "; ".join(Sequences_available),
                "SampleRep": "Not provided",
                "ReplicateMaterialSampleID": plutoF_data["Material_Sample_ID"],
            }
        )
        NonMatchingSamplingEventData.append({"EventID": plutoF_data["Parent_Event_ID"]})

for row in main_csv_data:
    # get the Event_ID
    event_id_to_compare = row["Event_ID"]
    isfound = False
    for sampling_event in SamplingEventData:
        sampling_event_id = sampling_event["EventID"]
        # print("event id to compare: " + event_id_to_compare)
        if event_id_to_compare == sampling_event_id:
            isfound = True
            print("found")
            break
    if isfound == False:
        print("not found")
        NonMatchingSamplingEventData.append({"EventID": event_id_to_compare})

# for sampling event in SamplingEventData:
# check the value of the sequencing run repeat
# if first sequencing run -> append _s1 to tge event id
# if second sequencing run (repeat) -> append _s2 to the event id

for sampling_event in SamplingEventData:
    if sampling_event["SequencingRunRepeat"] == "first sequencing run":
        sampling_event["ReplicateMaterialSampleID"] = (
            sampling_event["ReplicateMaterialSampleID"] + "_r1"
        )
    if sampling_event["SequencingRunRepeat"] == "second sequencing run (repeat)":
        sampling_event["ReplicateMaterialSampleID"] = (
            sampling_event["ReplicateMaterialSampleID"] + "_r2"
        )

for sampling_event in SamplingEventData:
    # if SampleRep is not empty , append the value to the EventID like _value
    if sampling_event["SampleRep"] != "Not provided":
        sampling_event["ReplicateMaterialSampleID"] = (
            sampling_event["ReplicateMaterialSampleID"]
            + "_"
            + sampling_event["SampleRep"]
        )

##OmicsData
# EventID gsheets["Event-ID"]
# MaterialSampleID gsheets["MaterialSample-ID"]
# OriginalSampleID gsheets["OriginalSample-ID"]
# Gene_COI gsheets["gene_COI"]
# GeneNegControl_COI gsheets["gene_COI_negative_control"]
# GeneITS gsheets["gene_ITS"]
# GeneNegControl_ITS gsheets["gene_ITS_negative_control"]
# Gene18S gsheets["gene_18S"]
# GeneNegControl_18S gsheets["gene_18S_negative_control"]
for gsheets_data in json_arms_samples_gsheets:
    # if (Gene_COI == undefined or  Gene_COI = "") and (GeneITS = "" or GeneITS == undefined ) and (Gene18S = "" or Gene18S == undefined):
    if (
        (
            gsheets_data["gene_COI"] == ""
            or gsheets_data["gene_COI"] == "undefined"
            or gsheets_data["gene_COI"] == "none"
        )
        and (
            gsheets_data["gene_ITS"] == ""
            or gsheets_data["gene_ITS"] == "undefined"
            or gsheets_data["gene_ITS"] == "none"
        )
        and (
            gsheets_data["gene_18S"] == ""
            or gsheets_data["gene_18S"] == "undefined"
            or gsheets_data["gene_18S"] == "none"
        )
    ):
        continue
    else:
        OmicsData.append(
            {
                "EventID": gsheets_data["Event-ID"],
                "MaterialSampleID": gsheets_data["MaterialSample-ID"],
                "Gene_COI": gsheets_data["gene_COI"],
                "Gene_COI_negative_control": gsheets_data["gene_COI_negative_control"],
                "Gene_COI_demultiplexed": gsheets_data["COI_demultiplexed"],
                "Gene_COI_comment": gsheets_data["comment_COI"],
                "Gene_ITS": gsheets_data["gene_ITS"],
                "Gene_ITS_negative_control": gsheets_data["gene_ITS_negative_control"],
                "Gene_ITS_demultiplexed": gsheets_data["ITS_demultiplexed"],
                "Gene_ITS_comment": gsheets_data["comment_ITS"],
                "Gene_18S": gsheets_data["gene_18S"],
                "Gene_18S_negative_control": gsheets_data["gene_18S_negative_control"],
                "Gene_18S_demultiplexed": gsheets_data["18S_demultiplexed"],
                "Gene_18S_comment": gsheets_data["comment_18S"],
                "OriginalSampleID": gsheets_data["OriginalSample-ID"],
                "SequencingRunRepeat": gsheets_data["SequencingRunRepeat"],
                "SequencingRunComment": gsheets_data["SequencingRunComment"],
                "SampleRep": gsheets_data["SampleRep"],
                "ReplicateMaterialSampleID": gsheets_data["MaterialSample-ID"],
            }
        )

for omics_data in OmicsData:
    # if SampleRep is not empty , append the value to the EventID like _value
    if omics_data["SampleRep"] != "Not provided":
        omics_data["ReplicateMaterialSampleID"] = (
            omics_data["ReplicateMaterialSampleID"] + "_" + omics_data["SampleRep"]
        )

for omics_data in OmicsData:
    if omics_data["SequencingRunRepeat"] == "first sequencing run":
        omics_data["ReplicateMaterialSampleID"] = (
            omics_data["ReplicateMaterialSampleID"] + "_r1"
        )
    if omics_data["SequencingRunRepeat"] == "second sequencing run (repeat)":
        omics_data["ReplicateMaterialSampleID"] = (
            omics_data["ReplicateMaterialSampleID"] + "_r2"
        )


##ImageData
# ObservatoryID gsheets["Observatory-ID (corrected)"]
# UnitID gsheets["ARMS-ID (corrected)"]
# EventID gsheets["Event-ID"]
# go over accomsiated data files, if item["EventID"] == gsheets["Event-ID"] and item["file_type"] == "image", append
# Filename item["File_Name"]
# Filetype item["File_Type"]
# Download URL item["File_Download_URL"]
for gsheets_data in json_arms_samples_gsheets:
    print(gsheets_data)
    for item in associated_csv_data:
        if item["Event_id"] == gsheets_data["Event-ID"]:
            ImageData.append(
                {
                    "ObservatoryID": gsheets_data["Observatory-ID"],
                    "UnitID": gsheets_data["ARMS-ID"],
                    "EventID": gsheets_data["Event-ID"],
                    "Filename": item["File_Name"],
                    "Filetype": item["File_Type"],
                    "PlateNumber": item["Plate_Number"],
                    "Position": item["Position"],
                    "Download URL": item["File_Download_URL"],
                }
            )
# go over the ImageData list and remove duplicates
ImageData = [dict(t) for t in {tuple(d.items()) for d in ImageData}]

# Create OtherData
OtherData = [item for item in ImageData if item["Filetype"] != "Image"]

# create mask to remove rows with file_type != "Image"
ImageData = [item for item in ImageData if item["Filetype"] == "Image"]

SamplingEventData = [dict(t) for t in {tuple(d.items()) for d in SamplingEventData}]
ObservatoryData = [dict(t) for t in {tuple(d.items()) for d in ObservatoryData}]
OmicsData = [dict(t) for t in {tuple(d.items()) for d in OmicsData}]
# write the data to csv files in the output directory
with open(
    os.path.join(output_dir, "combined_SamplingEventData.csv"),
    "w",
    newline="",
    encoding="utf-8",
) as f:
    w = csv.DictWriter(f, SamplingEventData[0].keys())
    w.writeheader()
    for row in SamplingEventData:
        print(row)
        # row = {k: v.encode('cp850','replace').decode('cp850') for k, v in row.items()}
        w.writerow(row)

# Write OtherData to a new file
with open(
    os.path.join(output_dir, "combined_OtherDataFiles.csv"),
    "w",
    newline="",
    encoding="utf-8",
) as f:
    w = csv.DictWriter(f, OtherData[0].keys())
    w.writeheader()
    for row in OtherData:
        w.writerow(row)

with open(
    os.path.join(output_dir, "combined_ObservatoryData.csv"),
    "w",
    newline="",
    encoding="utf-8",
) as f:
    w = csv.DictWriter(f, ObservatoryData[0].keys())
    w.writeheader()
    for row in ObservatoryData:
        # row = {k: v.encode('cp850','replace').decode('cp850') for k, v in row.items()}
        w.writerow(row)

with open(
    os.path.join(output_dir, "combined_OmicsData.csv"),
    "w",
    newline="",
    encoding="utf-8",
) as f:
    w = csv.DictWriter(f, OmicsData[0].keys())
    w.writeheader()
    for row in OmicsData:
        # row = {k: v.encode('cp850','replace').decode('cp850') for k, v in row.items()}
        w.writerow(row)

with open(
    os.path.join(output_dir, "combined_ImageData.csv"),
    "w",
    newline="",
    encoding="utf-8",
) as f:
    w = csv.DictWriter(f, ImageData[0].keys())
    w.writeheader()
    for row in ImageData:
        # row = {k: v.encode('cp850','replace').decode('cp850') for k, v in row.items()}
        w.writerow(row)

with open(
    os.path.join(output_dir, "in_plutoF_not_GS.csv"), "w", newline="", encoding="utf-8"
) as f:
    w = csv.DictWriter(f, NonMatchingSamplingEventData[0].keys())
    w.writeheader()
    for row in NonMatchingSamplingEventData:
        # row = {k: v.encode('cp850','replace').decode('cp850') for k, v in row.items()}
        w.writerow(row)
# cut the combined csv files to the ./Combined directory
for file in os.listdir(output_dir):
    if file.startswith("combined_"):
        # make the string of the file path to move
        # split the output_dir string on the os sep and pop the last element and rejoin the string by os.sep
        parent_folder = os.sep.join(output_dir.split(os.sep)[:-1])
        shutil.move(
            os.path.join(output_dir, file),
            os.path.join(parent_folder, "combined", file),
        )
