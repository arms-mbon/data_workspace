#do imports 
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
#from dotenv import load_dotenv
import pandas as pd
#import lib for sending mails
from smtplib import SMTP
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase

# variables here
#load_dotenv()
#print(os.getenv('SENDER_EMAIL'))
#print(os.getenv('PASSWORD'))
#sender_email = str(os.getenv('SENDER_EMAIL'))
#password = str(os.getenv('PASSWORD'))
#receiver_email = str(os.getenv('RECIEVER_EMAIL'))
# Creating the respective object along with the gmail login and port number
smtp_port = SMTP("smtp.gmail.com", 587)
# Establishing a connection to the SMTP server with Transport Layer Security (TLS) mode
#smtp_port.ehlo()
# Informing the client to establish a secure connection, either to a TLS or SSL
#smtp_port.starttls()
# Logging into your account
#smtp_port.login(sender_email , password)
# Creating the contents of the email
subject = "ARMS QC automated report"
#address_list = [receiver_email, "cedric.decruw@vliz.be"]

html_begin = """\
<html>
  <body>
    <p>Hi,<br>
        A summary of the QC script is below:<br>
    </p>
    <ul><br>
"""
html_end = """\
    <br>
    </ul>
    <br>
    <p> the qc report for for the arms observatories are as follows:</p><br>
    <ul>
    <li>
    <a href="https://github.com/arms-mbon/Data/blob/main/QualityControlledData/FromGS/qc_report_arms_observatories_gsheets_to_plutoF.csv">qc_report_arms_observatories_gsheets_to_plutoF.csv</a>
    </li>
    <li>
    <a href="https://github.com/arms-mbon/Data/blob/main/QualityControlledData/FromGS/qc_report_arms_observatories_plutoF_to_gsheets.csv">qc_report_arms_observatories_plutoF_to_gsheets.csv</a>
    </li>
    <li>
    <a href="https://github.com/arms-mbon/Data/blob/main/QualityControlledData/FromGS/qc_report_arms_samples_plutoF_to_gsheets.csv">qc_report_arms_samples_plutoF_to_gsheets.csv</a>
    </li>
    <li>
    <a href="https://github.com/arms-mbon/Data/blob/main/QualityControlledData/FromGS/qc_report_arms_samples_gsheets_to_plutoF.csv">qc_report_arms_samples_gsheets_to_plutoF.csv</a>
    </li>
    </ul>
    <br>
    <p>This mail was send by python QC-script<br></p>
  </body>
</html>
"""
pre_formatted_message = [html_begin]
message = MIMEMultipart("alternative")
message["Subject"] = subject
#message["From"] = sender_email
#message["To"] = receiver_email

#import json file names ./ARMS_data.json
#get parent dir of current file 
parent_dit = os.path.dirname(os.path.abspath(__file__))
output_dir = parent_dit

#download the plutoF josn dump 
plutoF_url_dmp = 'https://files.plutof.ut.ee/orig/5653762731985736347A39F3C37A593634BBA850A11BF35D5BFE1229CC6F10B3.json?h=GVqPsmf4XL9HGDRkWvxatw&e=1680170392'
plutoF_json_dmp = os.path.join(output_dir, 'AllARMSPlutof.json')
#download the plutoF josn dump 
file_dump = requests.get(plutoF_url_dmp, allow_redirects=True)
#pyt the file dump in the output dir
with open(plutoF_json_dmp, 'wb') as f:
    f.write(file_dump.content)

#load json file
json_data = open(os.path.join(parent_dit, 'AllARMSPlutof.json'))
json_data_loaded = json.load(json_data)

#load in csv file PlutoF_QC_v2_StationARMSnames.csv
with open(os.path.join(parent_dit, 'PlutoF_QC_StationARMSnames.csv'), 'r') as f:
    qc_stations = list(csv.reader(f))
#print(qc_stations)

#variables that will make the csv files
csv_file_QC_output = []

#helper function that will convert input date format 2021-05-15 18:53:34.831045+00:00 to format 2021-05-15
def converteddate(date):
    try:
        new_date = date.split(' ')[0]
        return new_date
    except:
        return date
    
def getDepth(child_area):
    #check if measurements are presentr in the child area
    try:
        if child_area['measurements']:
            #loop over the measurements and check if measurements[i]['measurement][name] == 'Depth max'
            i = 0
            for measurements in child_area['measurements']:
                if measurements['measurement']['name'] == 'Depth max':
                    #if so return the measurement value
                    return child_area['measurements'][i]['value']
                i+=1
        else:
            return 'no measurements'
    except:
        return 'no measurements'

#hepler functions that takes in input and also input column and return the value of the "input column corrected" from the qc-stations csv file if the value is not blank
def correctedvalue(input_value, input_column, input_country=None, input_station=None):
    index_column = 0
    for field in qc_stations[0]:
        if field == input_column:
            tocheckcolumn = index_column
        if field == input_column +' corrected':
            correctedcolumn = index_column
        index_column += 1
    
    toreturn = input_value
    found_station = False
    for row in qc_stations:
        if row[tocheckcolumn] == input_value:
            found_station = True
            if row[correctedcolumn] != '' and row[correctedcolumn] != ' ' and row[correctedcolumn] != None :
                correction_found = True
                #print(f'corrected value found for {input_value} in {input_column} column => {row[correctedcolumn]}')
                toreturn = row[correctedcolumn]
                #add to csv file
                if input_column == "Country":
                    csv_file_QC_output.append({'station': 'NA', 'country': toreturn, 'unit': 'NA', 'qc_param': input_column, 'qc_flag': 'passed'})
                elif input_column == "Station":
                    csv_file_QC_output.append({'station': toreturn, 'country': input_country, 'unit': 'NA', 'qc_param': input_column, 'qc_flag': 'passed'})
                elif input_column == "ARMS unit":
                    csv_file_QC_output.append({'station': input_station, 'country': input_country, 'unit': toreturn, 'qc_param': input_column, 'qc_flag': 'passed'})
            else:
                #print('no corrected value for ' + input_value)
                toreturn = input_value
            
    if found_station == False:
        correction_found = True
        if input_column == 'Station':
            csv_file_QC_output.append({'station': input_value, 'country': input_country, 'unit': 'NA', 'qc_param': input_column, 'qc_flag': 'missing'})
        elif input_column == 'Country':
            csv_file_QC_output.append({'station': 'NA', 'country': input_value, 'unit': 'NA', 'qc_param': input_column, 'qc_flag': 'missing'})
        elif input_column == 'ARMS unit':
            csv_file_QC_output.append({'station': input_station, 'country': input_country, 'unit': input_value, 'qc_param': input_column, 'qc_flag': 'missing'})
        part_attachted = '<li> - '+input_value + ' not found in column '+ input_column +' in the csv file </li>'
        pre_formatted_message.append(part_attachted)
    return toreturn


#get the following variables from the json file
#sampling areas ids
sampling_areas_ids = []
#child_areas_ids
child_areas_ids = []
#get all sampling_event_ids
sampling_event_ids = []
for sampling_area in json_data_loaded['sampling_areas']:
    sampling_areas_ids.append(sampling_area['id'])
    for child_area in sampling_area['child_areas']:
        child_areas_ids.append(child_area['id'])
        for sampling_event in child_area['sampling_events']:
            sampling_event_ids.append(sampling_event['id'])
        
#make the following csv files
# Main.csv => Station, Country, ARMS_unit, Date_start, Date_end, Event_description, Material Samples, Observations, Sequences, Associated Date, Created, Updated
main_csv_data = []
sequences_csv_data = []
associated_csv_data = []
observations_csv_data = []
material_samples_csv_data = []
correction_found = False
#make sample area name by replcing space with underscore
for sampling_area in json_data_loaded['sampling_areas']:
    ew_sampling_area_name = sampling_area['name'].replace(" ", "_")
    material_samples_csv = []
    observations_csv = []
    sequences_csv = []
    associated_data_csv = []
    main_data_csv = []
    try:
        os.mkdir(os.path.join(output_dir, ew_sampling_area_name))
    except Exception as e:
        print(e)
    #country
    country = correctedvalue(sampling_area['country'], 'Country')
    
    station = correctedvalue(sampling_area['name'], 'Station',input_country=sampling_area['country'])
    #print(f"working on {sampling_area['name']}")
    #print(f'working on {station}')
    for child_area in sampling_area['child_areas']:
        #print(f" area name {child_area['name']}")
        pre_ARMS_unit = correctedvalue(child_area['name'], 'ARMS unit',input_country=country, input_station=station)
        if pre_ARMS_unit == ' ' or pre_ARMS_unit == '' or pre_ARMS_unit == None:
            pre_ARMS_unit = child_area['name']
        #print(pre_ARMS_unit)
        #pre_ARMS_unit = pre_ARMS_unit.replace(station,'')
        pre_ARMS_unit = pre_ARMS_unit.replace('_', '')
        pre_ARMS_unit = pre_ARMS_unit.replace('ARMS', '')
        ARMS_unit = pre_ARMS_unit
        
        #get latitude longitude and depth
        latitude = child_area['latitude']
        longitude = child_area['longitude']
        depth = getDepth(child_area)
        
        for sampling_event in child_area['sampling_events']:
            #date_start
            date_start = converteddate(sampling_event['timespan_begin'])
            #date_end
            date_end = converteddate(sampling_event['timespan_end'])
            #event_id
            event_id = sampling_event['id']
            
            #get the habitat data 
            
            habitat = sampling_event['habitat']
            
            #try and get the desciption and iucn_habitat_type
            try:
                description = habitat['description']
            except:
                description = 'NA'
            
            try:
                iucn_habitat_type = habitat['iucn_habitat_type']
            except:
                iucn_habitat_type = "NA"
            
            #event_description
            try:
                date_end_desc = date_end.replace('-', '')
                date_start_desc = date_start.replace('-', '')
                if len(date_end.replace('-','')) != 8:
                    date_end_desc = "00000000"
                if len(date_start.replace('-','')) != 8:
                    date_start_desc = "00000000"
                event_description = "ARMS_" + station + '_' + ARMS_unit + '_' + date_start_desc + "_" + date_end_desc
            except:
                event_description = "ARMS_" + station + '_' + ARMS_unit + '_' + "00000000" + "_" + "00000000"
            #material_samples
            material_samples = len(sampling_event['material_samples'])
            #observations
            observations = len(sampling_event['observations'])
            #sequences
            sequences = len(sampling_event['sequences'])
            #associated_date
            associated_date = len(sampling_event['files'])
            #created
            created = converteddate(sampling_event['created_at'])
            #updated
            updated = converteddate(sampling_event['updated_at'])
            
            #material_sample table here
            for material_sample in sampling_event['material_samples']:
                sample_id = material_sample['id']
                sample_description = material_sample['description']
                material_sample_id = material_sample['name']
                sample_id_created_at = converteddate(material_sample['created_at'])
                sample_id_updated_at = converteddate(material_sample['updated_at'])
                sequences_in_sample = 0
                for sequence in sampling_event['sequences']:
                    if sequence["object_id"] == sample_id:
                        sequences_in_sample += 1
                material_samples_csv.append({'Material_Sample_ID': material_sample_id,"Parent_Event_ID": event_description,"Description": sample_description, "Created_At": sample_id_created_at, "Updated_At": sample_id_updated_at, "Sequences": sequences_in_sample, "Associated data": associated_date})
                material_samples_csv_data.append({'Material_Sample_ID': material_sample_id,"Parent_Event_ID": event_description,"Description": sample_description, "Created_At": sample_id_created_at, "Updated_At": sample_id_updated_at, "Sequences": sequences_in_sample, "Associated data": associated_date})
                
            #observation table here
            for observation in sampling_event['observations']:
                observation_id = observation['id']
                observation_remarks = observation['remarks']
                observation_is_varified = observation['moderation_status']
                for determination in observation['determinations']:
                    observation_updated_at = converteddate(determination['updated_at'])
                    observation_created_at = converteddate(determination['created_at'])
                    taxon_name = determination['taxon_node']
                    observations_csv.append({
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
                        "updated_at": observation_updated_at
                    })
                    observations_csv_data.append({
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
                        "updated_at": observation_updated_at
                    })
            
            #sequences table here
            for sequence in sampling_event['sequences']:
                sequence_id = sequence['id']
                sequence_updated_at = converteddate(sequence['updated_at'])
                sequence_created_at = converteddate(sequence['created_at'])
                sequence_sequence = sequence['sequence']
                sequence_chimeric = sequence['chimeric_status']
                sequence_unite_status = sequence['unite_status']
                sequence_low_quality = sequence['quality_status']
                sequence_forward_primer = sequence['forw_primer_sequence']
                sequence_reverse_primer = sequence['rev_primer_sequence']
                sequence_remarks = sequence['remarks']
                sequence_regions = ";".join(sequence['regions'])
                sequences_csv.append({
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
                    "updated_at": sequence_updated_at
                })
                sequences_csv_data.append({
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
                    "updated_at": sequence_updated_at
                })
                
            #associated_data table here
            for file in sampling_event['files']:   
                file_name = file['identifier'] 
                file_type = file['type']
                file_download_url = file['download_link']
                if file_download_url == None or file_download_url == "":
                    file_download_url = "Closed Access"
                associated_data_csv.append({
                    "Station": station,
                    "Country": country,
                    "ARMS_unit": ARMS_unit,
                    "date_start": date_start,
                    "date_end": date_end,
                    "Event_id": event_description,
                    "File_Name": file_name,
                    "File_Type": file_type,
                    "File_Download_URL": file_download_url,
                    "created_at": created,
                    "updated_at": updated
                })
                associated_csv_data.append({
                    "Station": station,
                    "Country": country,
                    "ARMS_unit": ARMS_unit,
                    "date_start": date_start,
                    "date_end": date_end,
                    "Event_id": event_description,
                    "File_Name": file_name,
                    "File_Type": file_type,
                    "File_Download_URL": file_download_url,
                    "created_at": created,
                    "updated_at": updated
                })
                
            main_csv_data.append(
                {'Station': station,
                 'Country': country,
                 'ARMS_unit': ARMS_unit,
                 'Latitude': latitude,
                 'Longitude': longitude,
                 'Depth': depth,
                 'Date_start': date_start,
                 'Date_end': date_end,
                 'Event_ID': event_description,
                 'Material Samples': material_samples,
                 'Observations': observations,
                 'Sequences': sequences,
                 'Associated Data': associated_date,
                 'Created': created,
                 'Updated': updated
                 })

            main_data_csv.append(
                {'Station': station,
                 'Country': country,
                 'ARMS_unit': ARMS_unit,
                 'Latitude': latitude,
                 'Longitude': longitude,
                 'Depth': depth,
                 'Date_start': date_start,
                 'Date_end': date_end,
                 'Event_ID': event_description,
                 'Event_Description': description,
                 "IUCN_Habitat_type": iucn_habitat_type,
                 'Material Samples': material_samples,
                 'Observations': observations,
                 'Sequences': sequences,
                 'Associated Data': associated_date,
                 'Created': created,
                 'Updated': updated
                 })
            
    

    with open(os.path.join(output_dir, ew_sampling_area_name,"material_samples_"+station+'.csv'), 'w', newline='') as csvfile:
        fieldnames = ['Material_Sample_ID', 'Parent_Event_ID', 'Description', 'Created_At', 'Updated_At', 'Sequences', 'Associated data']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in material_samples_csv:
            writer.writerow(data)
    
    with open(os.path.join(output_dir, ew_sampling_area_name,"observations_"+station+'.csv'), 'w', newline='') as csvfile:
        fieldnames = ['Station', 'Country', 'ARMS_unit', 'date_start', 'date_end', 'Event_id', 'Remarks', 'Is_Varified', 'Taxon_Name', 'created_at', 'updated_at']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in observations_csv:
            writer.writerow(data)
    
    with open(os.path.join(output_dir, ew_sampling_area_name,"sequences_"+station+'.csv'), 'w', newline='') as csvfile:
        fieldnames = ['Station', 'Country', 'ARMS_unit', 'date_start', 'date_end', 'Event_id', 'Sequence_ID', 'Sequence', 'Chimeric', 'Unite_Status', 'Low_Quality', 'Forward_Primer', 'Reverse_Primer', 'Remarks', 'Regions', 'created_at', 'updated_at']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in sequences_csv:
            writer.writerow(data)
            
    with open(os.path.join(output_dir, ew_sampling_area_name,"associated_data_"+station+'.csv'), 'w', newline='') as csvfile:
        fieldnames = ['Station', 'Country', 'ARMS_unit', 'date_start', 'date_end', 'Event_id', 'File_Name', 'File_Type', 'File_Download_URL', 'created_at', 'updated_at']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in associated_data_csv:
            #decode all the binary values in the data dict by utf-8 and encode them to cp850 and then decode again by cp580
            #
            data = {k: v.encode('cp850','replace').decode('cp850') for k, v in data.items()}
            writer.writerow(data)
    
    with open(os.path.join(output_dir, ew_sampling_area_name,"overview_data_"+station+'.csv'), 'w', newline='') as csvfile:
        fieldnames = ['Station', 'Country', 'ARMS_unit','Latitude','Longitude','Depth', 'Date_start', 'Date_end', 'Event_ID', 'Event_Description','IUCN_Habitat_type','Material Samples', 'Observations', 'Sequences', 'Associated Data', 'Created', 'Updated']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in main_data_csv:
            data = {k: str(v).encode('cp850','replace').decode('cp850') for k, v in data.items()}
            writer.writerow(data)

#write the main.csv
with open(os.path.join(output_dir, 'AllOverview.csv'), 'w', newline='') as csvfile:
    fieldnames = ['Station', 'Country', 'ARMS_unit','Latitude','Longitude','Depth', 'Date_start', 'Date_end', 'Event_ID', 'Material Samples', 'Observations', 'Sequences', 'Associated Data', 'Created', 'Updated']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in main_csv_data:
        writer.writerow(data)

#write the associated.csv
with open(os.path.join(output_dir, 'AllAssociatedData.csv'), 'w', newline='') as csvfile:
    fieldnames = ['Station', 'Country', 'ARMS_unit', 'date_start', 'date_end', 'Event_id', 'File_Name', 'File_Type', 'File_Download_URL', 'created_at', 'updated_at']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in associated_csv_data:
        data = {k: v.encode('cp850','replace').decode('cp850') for k, v in data.items()}
        writer.writerow(data)

#write the sequences.csv
with open(os.path.join(output_dir, 'AllSequences.csv'), 'w', newline='') as csvfile:
    fieldnames = ['Station', 'Country', 'ARMS_unit', 'date_start', 'date_end', 'Event_id', 'Sequence_ID', 'Sequence', 'Chimeric', 'Unite_Status', 'Low_Quality', 'Forward_Primer', 'Reverse_Primer', 'Remarks', 'Regions', 'created_at', 'updated_at']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in sequences_csv_data:
        writer.writerow(data)

#write the observations.csv
with open(os.path.join(output_dir, 'AllObservations.csv'), 'w', newline='') as csvfile:
    fieldnames = ['Station', 'Country', 'ARMS_unit', 'date_start', 'date_end', 'Event_id', 'Remarks', 'Is_Varified', 'Taxon_Name', 'created_at', 'updated_at']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in observations_csv_data:
        writer.writerow(data)
        
#write the material_samples.csv
with open(os.path.join(output_dir, 'AllMaterialSamples.csv'), 'w', newline='') as csvfile:
    fieldnames = ['Material_Sample_ID', 'Parent_Event_ID', 'Description', 'Created_At', 'Updated_At', 'Sequences', 'Associated data']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in material_samples_csv_data:
        writer.writerow(data)

filename = 'PlutoF_HarvestQCreport.csv'  # In same directory as script

#make csv file from csv_file_QC_output
with open(os.path.join(output_dir, filename), 'w', newline='') as csvfile:
    fieldnames = ['station','country','unit','qc_param','qc_flag']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in csv_file_QC_output:
        writer.writerow(data)

# Open PDF file in binary mode
with open(os.path.join(output_dir, filename), "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Add attachment to message and convert message to string
message.attach(part)
#Send email part#
pre_formatted_message.append(html_end)
formatted_message = ''.join(pre_formatted_message)
message.attach(MIMEText(formatted_message, "html"))
print(message)
#smtp_port.sendmail(sender_email, address_list, message.as_string()) #put on end script
print("Email Sent")
smtp_port.quit()

#perform a download of a google sheet and import each sheet as a json file : url = https://docs.google.com/spreadsheets/d/1j3yuY5lmoPMo91w6e3kkJ6pmp1X6FVGUtLealuKJ3wE/edit#gid=1607535453
url = 'https://docs.google.com/spreadsheets/d/1j3yuY5lmoPMo91w6e3kkJ6pmp1X6FVGUtLealuKJ3wE/export?format=csv&id=1j3yuY5lmoPMo91w6e3kkJ6pmp1X6FVGUtLealuKJ3wE&gid=1607535453'
r = requests.get(url, allow_redirects=True)
print(r.status_code)
with open(os.path.join(output_dir, "GS_ARMS_Observatory.csv"), "wb") as f:
        f.write(r.content)

#same for the arms_samples_sequences
url = 'https://docs.google.com/spreadsheets/d/1j3yuY5lmoPMo91w6e3kkJ6pmp1X6FVGUtLealuKJ3wE/export?format=csv&id=1j3yuY5lmoPMo91w6e3kkJ6pmp1X6FVGUtLealuKJ3wE&gid=855411053'
r = requests.get(url, allow_redirects=True)
with open(os.path.join(output_dir, "GS_ARMS_Samples_Sequences.csv"), "wb") as f:
        f.write(r.content)

#same for the arms observatory metadata
url = 'https://docs.google.com/spreadsheets/d/1j3yuY5lmoPMo91w6e3kkJ6pmp1X6FVGUtLealuKJ3wE/export?format=csv&id=1j3yuY5lmoPMo91w6e3kkJ6pmp1X6FVGUtLealuKJ3wE&gid=2133798758'
r = requests.get(url, allow_redirects=True)
with open(os.path.join(output_dir, "GS_ARMS_Observatory_Metadata.csv"), "wb") as f:
        f.write(r.content)

#same for the arms material_samples and sequence info metadata
url = 'https://docs.google.com/spreadsheets/d/1j3yuY5lmoPMo91w6e3kkJ6pmp1X6FVGUtLealuKJ3wE/export?format=csv&id=1j3yuY5lmoPMo91w6e3kkJ6pmp1X6FVGUtLealuKJ3wE&gid=1582985605'
r= requests.get(url, allow_redirects=True)
with open(os.path.join(output_dir, "GS_ARMS_Material_Samples_Sequence_Metadata.csv"), "wb") as f:
    f.write(r.content)
        
#make a QC report for the ARMS Observatory info comparing data from AllObservations.csv and ARMS_Observatory_info.csv
qc_report_arms_observatories_plutoF_to_gsheets = []
qc_report_arms_observatories_gsheets_to_plutoF = []
qc_observatory_info = []
#load in Arms Observatory info as json file
def csv_to_json(csv_file_path):
    #create a dictionary
    data_dict = []
    #Step 2
    #open a csv file handler
    with open(csv_file_path, encoding = 'utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)
        #convert each row into a dictionary
        #and add the converted data to the data_variable
        for rows in csv_reader:
            data_dict.append(rows)
    return data_dict
            
json_arms_observatories_gsheets = csv_to_json(os.path.join(output_dir, "GS_ARMS_Observatory.csv")) 
json_arms_observatories_plutoF = main_csv_data
#a mapping will be placed here in the future where all the culumbs are described that should be compared

#begin the plutoF to gsheets QC
for plutoF_data in json_arms_observatories_plutoF:
    found_observatory = False
    found_arms_id = False
    for gsheets_data in json_arms_observatories_gsheets:
        #check if the observatory name is the same
        try:
            if plutoF_data["Station"] == gsheets_data["Observatory-ID (corrected)"]:
                found_observatory = True
            #check if the arms_id is the same
            if plutoF_data["ARMS_unit"] == gsheets_data["ARMS-ID (corrected)"]:
                found_arms_id = True
            if found_arms_id == True and found_observatory == True:
                pass
        except:
            print("error")
    if found_arms_id == False:
        qc_observatory_info.append({"ARMS_unit": plutoF_data["ARMS_unit"], "Station": plutoF_data["Station"], "QC_comment": "ARMS ID not found in GS", "QC_param": "ARMS_ID", "QC_value_plutoF": plutoF_data["ARMS_unit"], "QC_value_gsheets": ""})
    if found_observatory == False:
        qc_observatory_info.append({"ARMS_unit": plutoF_data["ARMS_unit"], "Station": plutoF_data["Station"], "QC_comment": "Observatory not found in GS", "QC_param": "Observatory", "QC_value_plutoF": plutoF_data["Station"], "QC_value_gsheets": ""})
    

#same for gsheets to plutoF
for gsheets_data in json_arms_observatories_gsheets:
    found_observatory = False
    found_arms_id = False
    for plutoF_data in json_arms_observatories_plutoF:
        try:
            #check if the observatory name is the same
            if plutoF_data["Station"] == gsheets_data["Observatory-ID (corrected)"]:
                found_observatory = True
                
            #check if the arms_id is the same
            if plutoF_data["ARMS_unit"] == gsheets_data["ARMS-ID (corrected)"]:
                found_arms_id = True
            
            if found_arms_id == True and found_observatory == True:
                if abs(abs(float(plutoF_data["Latitude"])) - abs(float(gsheets_data["Latitude"]))) >  (0) or abs(float(plutoF_data["Longitude"]) - float(gsheets_data["Longitude"])) > (0):
                    if abs(abs(float(plutoF_data["Latitude"])) - abs(float(gsheets_data["Latitude"]))) >  (1/111.6) or abs(float(plutoF_data["Longitude"]) - float(gsheets_data["Longitude"])) > (1/111.6):
                        qc_observatory_info.append({"ARMS_unit": gsheets_data["ARMS-ID (corrected)"], "Station": gsheets_data["Country ISO3letter code"], "QC_comment": "Observatory and ARMS ID found but lat or long are SIGNIFICANTLY different", "QC_param": "Lat_Long", "QC_value_plutoF": plutoF_data["Latitude"] + " " + plutoF_data["Longitude"], "QC_value_gsheets": gsheets_data["Latitude"] + " " + gsheets_data["Longitude"]})
                    else:
                        qc_observatory_info.append({"ARMS_unit": gsheets_data["ARMS-ID (corrected)"], "Station": gsheets_data["Country ISO3letter code"], "QC_comment": "Observatory and ARMS ID found but lat and long are different", "QC_param": "Lat_Long", "QC_value_plutoF": plutoF_data["Latitude"] + " " + plutoF_data["Longitude"], "QC_value_gsheets": gsheets_data["Latitude"] + " " + gsheets_data["Longitude"]})   
                else:
                    qc_observatory_info.append({"ARMS_unit": gsheets_data["ARMS-ID (corrected)"], "Station": gsheets_data["Country ISO3letter code"], "QC_comment": "OK"})
                break
        except:
            pass
    if found_arms_id == False:
        qc_observatory_info.append({"ARMS_unit": gsheets_data["ARMS-ID (corrected)"], "Station": gsheets_data["Country ISO3letter code"], "QC_comment": "ARMS ID not found in PlutoF", "QC_param": "ARMS_ID", "QC_value_plutoF": "", "QC_value_gsheets": gsheets_data["ARMS-ID (corrected)"]})
    if found_observatory == False:
        qc_observatory_info.append({"ARMS_unit": gsheets_data["ARMS-ID (corrected)"], "Station": gsheets_data["Country ISO3letter code"], "QC_comment": "Observatory not found in PlutoF", "QC_param": "Observatory", "QC_value_plutoF": "", "QC_value_gsheets": gsheets_data["Country ISO3letter code"]})
    

#begin the plutoF to gsheets QC
for plutoF_data in json_arms_observatories_plutoF:
    found = False
    for gsheets_data in json_arms_observatories_gsheets:
        #begin with the rules 
        #if the arms_id is the same then begin checking the rules
        if plutoF_data["ARMS_unit"] == gsheets_data["ARMS-ID (corrected)"]:
            found = True
            #go over the rules
            #check if the lat; long and depth are the same
            try:
                if float(plutoF_data["Latitude"]) != float(gsheets_data["Latitude"]):
                    #check if the difference is less than 2m and if so then pass
                    if abs(abs(float(plutoF_data["Latitude"])) - abs(float(gsheets_data["Latitude"]))) >  (1/111.6):
                        qc_report_arms_observatories_plutoF_to_gsheets.append({"station":plutoF_data["Station"],"arms_unit":plutoF_data["ARMS_unit"], "qc_param":"latitude", "qc_flag":"fail","plutoF_data":plutoF_data["Latitude"], "gsheets_data":gsheets_data["Latitude"]})
                    else:
                        qc_report_arms_observatories_plutoF_to_gsheets.append({"station":plutoF_data["Station"],"arms_unit":plutoF_data["ARMS_unit"], "qc_param":"latitude", "qc_flag":"value is different but not significantly","plutoF_data":plutoF_data["Latitude"], "gsheets_data":gsheets_data["Latitude"]})
            except:
                qc_report_arms_observatories_plutoF_to_gsheets.append({"station":plutoF_data["Station"],"arms_unit":plutoF_data["ARMS_unit"], "qc_param":"latitude", "qc_flag":"fail","plutoF_data":plutoF_data["Latitude"], "gsheets_data":gsheets_data["Latitude"]})
            
            try:
                if float(plutoF_data["Longitude"]) != float(gsheets_data["Longitude"]):
                    if abs(abs(float(plutoF_data["Longitude"])) - abs(float(gsheets_data["Longitude"]))) >  (1/111.6):
                        qc_report_arms_observatories_plutoF_to_gsheets.append({"station":plutoF_data["Station"],"arms_unit":plutoF_data["ARMS_unit"], "qc_param":"longitude", "qc_flag":"fail","plutoF_data":plutoF_data["Longitude"], "gsheets_data":gsheets_data["Longitude"]})
                    else:
                        qc_report_arms_observatories_plutoF_to_gsheets.append({"station":plutoF_data["Station"],"arms_unit":plutoF_data["ARMS_unit"], "qc_param":"longitude", "qc_flag":"value is different but not significantly","plutoF_data":plutoF_data["Longitude"], "gsheets_data":gsheets_data["Longitude"]})
            except:
                qc_report_arms_observatories_plutoF_to_gsheets.append({"station":plutoF_data["Station"],"arms_unit":plutoF_data["ARMS_unit"], "qc_param":"longitude", "qc_flag":"fail","plutoF_data":plutoF_data["Longitude"], "gsheets_data":gsheets_data["Longitude"]})
                
            try:
                if float(plutoF_data["Depth"]) != float(gsheets_data["Depth (m)"]):
                    if abs(float(plutoF_data["Depth"]) - float(gsheets_data["Depth (m)"])) > 1:
                        qc_report_arms_observatories_plutoF_to_gsheets.append({"station":plutoF_data["Station"],"arms_unit":plutoF_data["ARMS_unit"], "qc_param":"depth", "qc_flag":"fail","plutoF_data":plutoF_data["Depth"], "gsheets_data":gsheets_data["Depth (m)"]})
            except:
                qc_report_arms_observatories_plutoF_to_gsheets.append({"station":plutoF_data["Station"],"arms_unit":plutoF_data["ARMS_unit"], "qc_param":"depth", "qc_flag":"fail","plutoF_data":plutoF_data["Depth"], "gsheets_data":gsheets_data["Depth (m)"]})
            
            try:
                if float(plutoF_data["Latitude"]) == float(gsheets_data["Latitude"]) and float(plutoF_data["Longitude"]) == float(gsheets_data["Longitude"]) and float(plutoF_data["Depth"]) == float(gsheets_data["Depth (m)"]):
                    qc_report_arms_observatories_plutoF_to_gsheets.append({"station":plutoF_data["Station"],"arms_unit":plutoF_data["ARMS_unit"], "qc_param":"latitude, longitude, depth", "qc_flag":"pass"})
            except:
                qc_report_arms_observatories_plutoF_to_gsheets.append({"station":plutoF_data["Station"],"arms_unit":plutoF_data["ARMS_unit"], "qc_param":"latitude, longitude, depth", "qc_flag":"pass"})
    if found == False:
        qc_report_arms_observatories_plutoF_to_gsheets.append({"station":plutoF_data["Station"],"arms_unit":plutoF_data["ARMS_unit"], "qc_param":"arms_unit", "qc_flag":"fail","plutoF_data":plutoF_data["ARMS_unit"], "gsheets_data":gsheets_data["ARMS-ID (corrected)"]})

#do the same for the gsheets to plutoF QC
for gsheets_data in json_arms_observatories_gsheets:
    found = False
    for plutoF_data in json_arms_observatories_plutoF:
        if gsheets_data["ARMS-ID (corrected)"] == plutoF_data["ARMS_unit"]:
            found = True
            #go over the rules
            try:
                if float(gsheets_data["Latitude"]) != float(plutoF_data["Latitude"]):
                    #if the first 2 characters after the . are the same then pass
                    if abs(abs(float(gsheets_data["Latitude"])) - abs(float(plutoF_data["Latitude"]))) > (1/111.6):
                        qc_report_arms_observatories_gsheets_to_plutoF.append({"station":gsheets_data["Observatory-ID (corrected)"],"arms_id":gsheets_data["ARMS-ID (corrected)"], "qc_param":"latitude", "qc_flag":"fail","gsheets_data":gsheets_data["Latitude"],"plutoF_data":plutoF_data["Latitude"]})
                    else:
                        qc_report_arms_observatories_gsheets_to_plutoF.append({"station":gsheets_data["Observatory-ID (corrected)"],"arms_id":gsheets_data["ARMS-ID (corrected)"], "qc_param":"latitude", "qc_flag":"value is different but not significantly","gsheets_data":gsheets_data["Latitude"],"plutoF_data":plutoF_data["Latitude"]})
            except:
                qc_report_arms_observatories_gsheets_to_plutoF.append({"station":gsheets_data["Observatory-ID (corrected)"],"arms_id":gsheets_data["ARMS-ID (corrected)"], "qc_param":"latitude", "qc_flag":"fail","gsheets_data":gsheets_data["Latitude"],"plutoF_data":plutoF_data["Latitude"]})
            try:
                if float(gsheets_data["Longitude"]) != float(plutoF_data["Longitude"]):
                    if abs(abs(float(gsheets_data["Longitude"])) - abs(float(plutoF_data["Longitude"]))) >  (1/111.6):
                        qc_report_arms_observatories_gsheets_to_plutoF.append({"station":gsheets_data["Observatory-ID (corrected)"],"arms_id":gsheets_data["ARMS-ID (corrected)"], "qc_param":"longitude", "qc_flag":"fail","gsheets_data":gsheets_data["Longitude"],"plutoF_data":plutoF_data["Longitude"]})
                    else:
                        qc_report_arms_observatories_gsheets_to_plutoF.append({"station":gsheets_data["Observatory-ID (corrected)"],"arms_id":gsheets_data["ARMS-ID (corrected)"], "qc_param":"longitude", "qc_flag":"value is different but not significantly","gsheets_data":gsheets_data["Longitude"],"plutoF_data":plutoF_data["Longitude"]})
            except:
                qc_report_arms_observatories_gsheets_to_plutoF.append({"station":gsheets_data["Observatory-ID (corrected)"],"arms_id":gsheets_data["ARMS-ID (corrected)"], "qc_param":"longitude", "qc_flag":"fail","gsheets_data":gsheets_data["Longitude"],"plutoF_data":plutoF_data["Longitude"]})
            try:
                if float(gsheets_data["Depth (m)"]) != float(plutoF_data["Depth"]):
                    if abs(float(gsheets_data["Depth (m)"]) - float(plutoF_data["Depth"])) > 1:
                        qc_report_arms_observatories_gsheets_to_plutoF.append({"station":gsheets_data["Observatory-ID (corrected)"],"arms_id":gsheets_data["ARMS-ID (corrected)"], "qc_param":"depth", "qc_flag":"fail","gsheets_data":gsheets_data["Depth (m)"],"plutoF_data":plutoF_data["Depth"]})
            except:
                qc_report_arms_observatories_gsheets_to_plutoF.append({"station":gsheets_data["Observatory-ID (corrected)"],"arms_id":gsheets_data["ARMS-ID (corrected)"], "qc_param":"depth", "qc_flag":"fail","gsheets_data":gsheets_data["Depth (m)"],"plutoF_data":plutoF_data["Depth"]})
            try:
                if float(gsheets_data["Latitude"]) == float(plutoF_data["Latitude"]) and float(gsheets_data["Longitude"]) == float(plutoF_data["Longitude"]) and float(gsheets_data["Depth (m)"]) == float(plutoF_data["Depth"]):
                    qc_report_arms_observatories_gsheets_to_plutoF.append({"station":gsheets_data["Observatory-ID (corrected)"],"arms_id":gsheets_data["ARMS-ID (corrected)"], "qc_param":"latitude, longitude, depth", "qc_flag":"pass"})
            except:
                qc_report_arms_observatories_gsheets_to_plutoF.append({"station":gsheets_data["Observatory-ID (corrected)"],"arms_id":gsheets_data["ARMS-ID (corrected)"], "qc_param":"latitude, longitude, depth", "qc_flag":"pass"})
    if found == False:
        qc_report_arms_observatories_gsheets_to_plutoF.append({"station":gsheets_data["Observatory-ID (corrected)"],"arms_id":gsheets_data["ARMS-ID (corrected)"], "qc_param":"arms_id", "qc_flag":"fail","gsheets_data":gsheets_data["ARMS-ID (corrected)"],"plutoF_data":plutoF_data["ARMS_unit"]})

#write away the reports to a csv file 
with open(os.path.join(output_dir, "qc_report_arms_observatories_plutoF_to_gsheets.csv"), "w", newline='') as f:
    fieldnames = ['station','arms_unit','qc_param','qc_flag','plutoF_data','gsheets_data']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for data in qc_report_arms_observatories_plutoF_to_gsheets:
        writer.writerow(data)

with open(os.path.join(output_dir, "qc_report_arms_observatories_gsheets_to_plutoF.csv"), "w", newline='') as f:
    fieldnames = ['station','arms_id','qc_param','qc_flag','gsheets_data','plutoF_data']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for data in qc_report_arms_observatories_gsheets_to_plutoF:
        writer.writerow(data)
        
with open(os.path.join(output_dir, "qc_report_observatory_info.csv"), "w", newline='') as f:
    fieldnames = ['ARMS_unit','Station','QC_comment','QC_param','QC_value_plutoF','QC_value_gsheets']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for data in qc_observatory_info:
        writer.writerow(data)
        

#perform the same qc for the samples
qc_report_arms_samples_plutoF_to_gsheets = []
qc_report_arms_samples_gsheets_to_plutoF = []

json_arms_samples_gsheets = csv_to_json(os.path.join(output_dir, "GS_ARMS_Samples_Sequences.csv")) 
json_arms_samples_plutoF = material_samples_csv_data
print(material_samples_csv_data)

#begin the plutoF to gsheets QC
for plutoF_data in json_arms_samples_plutoF:
    found = False
    #print(plutoF_data)
    for gsheets_data in json_arms_samples_gsheets:
        if plutoF_data["Parent_Event_ID"] == gsheets_data["Event-ID"]:
            found = True
    
    if found == False:
        qc_report_arms_samples_plutoF_to_gsheets.append({"sample":plutoF_data["Material_Sample_ID"],"qc_param":"event_id", "qc_flag":"fail","plutoF_data":plutoF_data["Parent_Event_ID"],"gsheets_data":"not found"})
    if found == True:
        sample_found = False
        for gsheets_data in json_arms_samples_gsheets:
            if plutoF_data["Material_Sample_ID"] == gsheets_data["MaterialSample-ID"]:
                sample_found = True
        if sample_found == False:
            qc_report_arms_samples_plutoF_to_gsheets.append({"sample":plutoF_data["Material_Sample_ID"],"qc_param":"sample_id", "qc_flag":"fail","plutoF_data":plutoF_data["Material_Sample_ID"],"gsheets_data":"not found"})

        if sample_found == True:
            qc_report_arms_samples_plutoF_to_gsheets.append({"sample":plutoF_data["Material_Sample_ID"],"qc_param":"sample_id", "qc_flag":"pass"})

#do the same for gsheets to plutoF
for gsheets_data in json_arms_samples_gsheets:
    found = False
    for plutof_data in json_arms_samples_plutoF:
        #first check if the event id is the same
        if gsheets_data["Event-ID"] == plutof_data["Parent_Event_ID"]:
            found = True
            
    if found == False:
        qc_report_arms_observatories_gsheets_to_plutoF.append({"sample":gsheets_data["MaterialSample-ID"],"qc_param":"event_id", "qc_flag":"fail","plutoF_data":"not found","gsheets_data":gsheets_data["Event-ID"]})

    if found == True:
        sample_found = False
        for plutof_data in json_arms_samples_plutoF:
            if gsheets_data["MaterialSample-ID"] == plutof_data["Material_Sample_ID"]:
                sample_found = True
        if sample_found == False:
            qc_report_arms_samples_gsheets_to_plutoF.append({"sample":gsheets_data["MaterialSample-ID"],"qc_param":"sample_id", "qc_flag":"fail","plutoF_data":"not found","gsheets_data":gsheets_data["MaterialSample-ID"]})
        if sample_found == True: 
            qc_report_arms_samples_gsheets_to_plutoF.append({"sample":gsheets_data["MaterialSample-ID"],"qc_param":"sample_id", "qc_flag":"pass"})
            
#make a qc report that will compare the events in plutoF to the events in gsheets
#the file will be called qc_report_events.csv
#The CSV can have columns: Event-ID from GS, Deployment Date from GS, Collection Date from GS, Event_id from PlutoF, Date_start from PlutoF, Date_end from PlutoF.
#if there is no PlutoF event for a GS, then the cell value under "Event_id from PlutoF" is "missing" and the date cell values can be blank/"missing".
#If there is no GS event for a Plutof, then the cell value under"Event-ID from GS" is "missing" and the date cell values can be blank/"missing".
#Note that while the date part of the Event-ID should be the same as the deployment and collection date values, 
#there is no guarantee that this will be so: hence we treat the EventID as the key as the dates as values 
#that I will manually compare to the date part of the EventID. So please do stick to the YYYY-MM-DD format. 

qc_events = []

#from plutoF to gsheets
for plutoF_data in main_csv_data:
    found = False
    for gs_data in json_arms_samples_gsheets:
        #check if the event id is the same
        if plutoF_data["Event_ID"] == gs_data["Event-ID"]:
            qc_events.append({"Event-ID from GS":gs_data["Event-ID"],"Deployment Date from GS":gs_data["Deployment Date"],"Collection Date from GS":gs_data["Collection Date"],"Event_id from PlutoF":plutoF_data["Event_ID"],"Date_start from PlutoF":plutoF_data["Date_start"],"Date_end from PlutoF":plutoF_data["Date_end"]})
            found = True
            break
    if found == False:
        qc_events.append({"Event-ID from GS":"missing","Deployment Date from GS":"missing","Collection Date from GS":"missing","Event_id from PlutoF":plutoF_data["Event_ID"],"Date_start from PlutoF":plutoF_data["Date_start"],"Date_end from PlutoF":plutoF_data["Date_end"]})

#from gsheets to plutoF
for gs_data in json_arms_samples_gsheets:
    found = False
    for plutoF_data in main_csv_data:
        if gs_data["Event-ID"] == plutoF_data["Event_ID"]:
            found = True
            present = False
            #check if the event id already in the list
            if len(qc_events) > 0:
                for qc_event in qc_events:
                    if qc_event["Event-ID from GS"] == gs_data["Event-ID"]:
                        present = True
                        break
            if present == False:
                qc_events.append({"Event-ID from GS":gs_data["Event-ID"],"Deployment Date from GS":gs_data["Deployment Date"],"Collection Date from GS":gs_data["Collection Date"],"Event_id from PlutoF":plutoF_data["Event_ID"],"Date_start from PlutoF":plutoF_data["Date_start"],"Date_end from PlutoF":plutoF_data["Date_end"]})
            break       
    if found == False:
        qc_events.append({"Event-ID from GS":gs_data["Event-ID"],"Deployment Date from GS":gs_data["Deployment Date"],"Collection Date from GS":gs_data["Collection Date"],"Event_id from PlutoF":"missing","Date_start from PlutoF":"missing","Date_end from PlutoF":"missing"})

#write the qc report to csv
with open(os.path.join(output_dir, 'qc_report_events.csv'), 'w', newline='', encoding="utf-8") as csvfile:
    fieldnames = ["Event-ID from GS","Deployment Date from GS","Collection Date from GS","Event_id from PlutoF","Date_start from PlutoF","Date_end from PlutoF"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in qc_events:
        writer.writerow(row)

#write both reports to csv
with open(os.path.join(output_dir, 'qc_report_arms_samples_plutoF_to_gsheets.csv'), 'w', newline='', encoding="utf-8") as csvfile:
    fieldnames = ["sample","qc_param","qc_flag","plutoF_data","gsheets_data"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in qc_report_arms_samples_plutoF_to_gsheets:
        writer.writerow(row)

with open(os.path.join(output_dir, 'qc_report_arms_samples_gsheets_to_plutoF.csv'), 'w', newline='', encoding="utf-8") as csvfile:
    fieldnames = ["sample","qc_param","qc_flag","plutoF_data","gsheets_data"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in qc_report_arms_samples_gsheets_to_plutoF:
        writer.writerow(row)
            
#cut all the files that start with GS_ARMS_ and end with .csv and put them in the parent folder of the output folder /FromGS
for file in os.listdir(output_dir):
    if file.startswith("GS_ARMS_") and file.endswith(".csv"):
        #make the string of the file path to move
        #split the output_dir string on the os sep and pop the last element and rejoin the string by os.sep
        parent_folder = os.sep.join(output_dir.split(os.sep)[:-1])
        shutil.move(os.path.join(output_dir,file),os.path.join(parent_folder,"FromGS",file))
        
#do the same for all the files that start with qc_report
for file in os.listdir(output_dir):
    if file.startswith("qc_report"):
        #make the string of the file path to move
        #split the output_dir string on the os sep and pop the last element and rejoin the string by os.sep
        parent_folder = os.sep.join(output_dir.split(os.sep)[:-1])
        shutil.move(os.path.join(output_dir,file),os.path.join(parent_folder,"FromGS",file))
        
#combine gsheets data with plutoF data in one file
SamplingEventData = []
NonMatchingSamplingEventData = []
ObservatoryData = []
OmicsData = []
ImageData = []

##ObservatoryData
#country from gsheets["Country ISO3letter code"]
#ObservatoryID gsheets["Observatory-ID (corrected)"]
#UnitID gsheets["ARMS-ID (corrected)"]
#Latitude gsheets["Latitude"]
#Longitude gsheets["Longitude"]
#Depth gsheets["Depth (m)"]
#Field Replicates gsheets["Field Replicates"]
#Monitoring area  gsheets["Monitoring area"]
#Habitat keywords gsheets["Habitat keywords (env_local)"]
for gsheets_data in json_arms_observatories_gsheets:
   ObservatoryData.append(
        {"Country":gsheets_data["Country ISO3letter code"],
         "ObservatoryID":gsheets_data["Observatory-ID (corrected)"],
         "UnitID":gsheets_data["ARMS-ID (corrected)"],
         "Latitude":gsheets_data["Latitude"],
         "Longitude":gsheets_data["Longitude"],
         "Depth":gsheets_data["Depth (m)"],
         "Field Replicates":gsheets_data["Field replicates"],
         "Monitoring area":gsheets_data["Monitoring area"],
         "Habitat keywords":gsheets_data["Habitat keywords (env_local)"]
         }
    )

##SamplingEventData
#country from gsheets["Country ISO3letter code"]
#ObservatoryID gsheets["Observatory-ID (corrected)"]
#UnitID gsheets["ARMS-ID (corrected)"]
#DateDeployed gsheets["Deployment Date"]
#DateCollected gsheets["Collection Date"]
#Event-ID gsheets["Event-ID"]
#MaterialSampleID gsheets["MaterialSample-ID"]
#Fraction gsheets["Fraction"]
#Preservative gsheets["Preservative"]
#Filter gsheets["Filter (micrometer)"]
#CrateCover gsheets["Crate cover used during retrieval"]
#Number of associated data files => for item in accomsiated data files, if item["Event-ID"] == gsheets["Event-ID"], count += 1
for gsheets_data in json_arms_samples_gsheets:
    count = 0
    for item in associated_csv_data:
        if item["Event_id"] == gsheets_data["Event-ID"]:
            count += 1
    
    for observatories in ObservatoryData:
        if gsheets_data["Observatory-ID"] == observatories["ObservatoryID"]:
            country = observatories["Country"]        
        
    #check if eventid is in the plutoF data
    for plutoF_data in material_samples_csv_data:
        #print(plutoF_data)
        #print(plutoF_data["Parent_Event_ID"])
        if gsheets_data["Event-ID"] == plutoF_data["Parent_Event_ID"]:       
            print("event id in plutoF data :"+ gsheets_data["Event-ID"])
            SamplingEventData.append(
                {"Country":country,
                "ObservatoryID":gsheets_data["Observatory-ID"],
                "UnitID":gsheets_data["ARMS-ID"],
                "DateDeployed":gsheets_data["Deployment Date"],
                "DateCollected":gsheets_data["Collection Date"],
                "EventID":gsheets_data["Event-ID"],
                "MaterialSampleID":gsheets_data["MaterialSample-ID"],
                "Fraction":gsheets_data["Fraction"],
                "Preservative":gsheets_data["Preservative"],
                "Filter":gsheets_data["Filter (micrometer)"],
                "CrateCover":gsheets_data["Crate cover used during retrieval"],
                "Number of associated data files":str(count)
                }
            )
        else:
            SamplingEventData.append(
                {"Country":country,
                "ObservatoryID":gsheets_data["Observatory-ID"],
                "UnitID":gsheets_data["ARMS-ID"],
                "DateDeployed":gsheets_data["Deployment Date"],
                "DateCollected":gsheets_data["Collection Date"],
                "EventID":gsheets_data["Event-ID"],
                "MaterialSampleID":gsheets_data["MaterialSample-ID"],
                "Fraction":gsheets_data["Fraction"],
                "Preservative":gsheets_data["Preservative"],
                "Filter":gsheets_data["Filter (micrometer)"],
                "CrateCover":gsheets_data["Crate cover used during retrieval"],
                "Number of associated data files":str(count)
                }
            )

for plutoF_data in material_samples_csv_data:
    inGoogleSheets = False
    for obs_plutoF_data in json_arms_observatories_plutoF:
        #get the country from the observatory data by matching the observatory id
        if obs_plutoF_data["Event_ID"] == plutoF_data["Parent_Event_ID"]:
            #get country from the observatory data
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
            print(gsheets_data["Event-ID"] + " is in google sheets")
    if inGoogleSheets == False:
        SamplingEventData.append(
            {"Country":country,
            "ObservatoryID":observatoryid,
            "UnitID":unitid,
            "DateDeployed":date_deployed,
            "DateCollected":collection_date,
            "EventID":plutoF_data["Parent_Event_ID"],
            "MaterialSampleID":plutoF_data["Material_Sample_ID"],
            "Fraction":gsheets_data["Fraction"],
            "Preservative":"Not provided",
            "Filter":"Not provided",
            "CrateCover":"Not provided",
            "Number of associated data files":plutoF_data["Associated data"]
            }
        )
        NonMatchingSamplingEventData.append(
            {
                "EventID":plutoF_data["Parent_Event_ID"]
            }
        )    
        
for row in main_csv_data:
    #get the Event_ID
    event_id_to_compare = row["Event_ID"]
    isfound = False
    for sampling_event in SamplingEventData:
        sampling_event_id = sampling_event["EventID"]
        #print("event id to compare: " + event_id_to_compare)
        if event_id_to_compare == sampling_event_id:
            isfound = True
            print("found")
            break
    if isfound == False:
        print("not found")
        NonMatchingSamplingEventData.append(
            {
                "EventID":event_id_to_compare
            }
        )

##OmicsData
#EventID gsheets["Event-ID"]
#MaterialSampleID gsheets["MaterialSample-ID"]
#OriginalSampleID gsheets["OriginalSample-ID"]
#Gene_COI gsheets["gene_COI"]
#GeneNegControl_COI gsheets["gene_COI_negative_control"]
#GeneITS gsheets["gene_ITS"]
#GeneNegControl_ITS gsheets["gene_ITS_negative_control"]
#Gene18S gsheets["gene_18S"]
#GeneNegControl_18S gsheets["gene_18S_negative_control"]
for gsheets_data in json_arms_samples_gsheets:
    #if (Gene_COI == undefined or  Gene_COI = "") and (GeneITS = "" or GeneITS == undefined ) and (Gene18S = "" or Gene18S == undefined):
    if (gsheets_data["gene_COI"] == "" or gsheets_data["gene_COI"] == "undefined") and (gsheets_data["gene_ITS"] == "" or gsheets_data["gene_ITS"] == "undefined") and (gsheets_data["gene_18S"] == "" or gsheets_data["gene_18S"] == "undefined"):
        continue
    else:
        OmicsData.append(
            {"EventID":gsheets_data["Event-ID"],
            "MaterialSampleID":gsheets_data["MaterialSample-ID"],
            "Gene_COI":gsheets_data["gene_COI"],
            "Gene_COI_negative_control":gsheets_data["gene_COI_negative_control"],
            "GeneITS":gsheets_data["gene_ITS"],
            "Gene_ITS_negative_control":gsheets_data["gene_ITS_negative_control"],
            "Gene18S":gsheets_data["gene_18S"],
            "Gene_18S_negative_control":gsheets_data["gene_18S_negative_control"],
            "OriginalSampleID":gsheets_data["OriginalSample-ID"]
            }
        )

##ImageData
#ObservatoryID gsheets["Observatory-ID (corrected)"]
#UnitID gsheets["ARMS-ID (corrected)"]
#EventID gsheets["Event-ID"]
#go over accomsiated data files, if item["EventID"] == gsheets["Event-ID"] and item["file_type"] == "image", append 
#Filename item["File_Name"]
#Filetype item["File_Type"]
#Download URL item["File_Download_URL"]
for gsheets_data in json_arms_samples_gsheets:
    for item in associated_csv_data:
        if item["Event_id"] == gsheets_data["Event-ID"]:
            ImageData.append(
                {"ObservatoryID":gsheets_data["Observatory-ID"],
                 "UnitID":gsheets_data["ARMS-ID"],
                 "EventID":gsheets_data["Event-ID"],
                 "Filename":item["File_Name"],
                 "Filetype":item["File_Type"],
                 "Download URL":item["File_Download_URL"]
                 }
            )

#go over the ImageData list and remove duplicates
ImageData = [dict(t) for t in {tuple(d.items()) for d in ImageData}]
SamplingEventData = [dict(t) for t in {tuple(d.items()) for d in SamplingEventData}]
ObservatoryData = [dict(t) for t in {tuple(d.items()) for d in ObservatoryData}]
OmicsData = [dict(t) for t in {tuple(d.items()) for d in OmicsData}]

#write the data to csv files in the output directory 
with open(os.path.join(output_dir,"combined_SamplingEventData.csv"), 'w', newline='', encoding="utf-8") as f:
    w = csv.DictWriter(f, SamplingEventData[0].keys())
    w.writeheader()
    for row in SamplingEventData:
        #row = {k: v.encode('cp850','replace').decode('cp850') for k, v in row.items()}
        w.writerow(row)

with open(os.path.join(output_dir,"combined_ObservatoryData.csv"), 'w', newline='', encoding="utf-8") as f:
    w = csv.DictWriter(f, ObservatoryData[0].keys())
    w.writeheader()
    for row in ObservatoryData:
        #row = {k: v.encode('cp850','replace').decode('cp850') for k, v in row.items()}
        w.writerow(row)

with open(os.path.join(output_dir,"combined_OmicsData.csv"), 'w', newline='', encoding="utf-8") as f:
    w = csv.DictWriter(f, OmicsData[0].keys())
    w.writeheader()
    for row in OmicsData:
        #row = {k: v.encode('cp850','replace').decode('cp850') for k, v in row.items()}
        w.writerow(row)

with open(os.path.join(output_dir,"combined_ImageData.csv"), 'w', newline='', encoding="utf-8") as f:
    w = csv.DictWriter(f, ImageData[0].keys())
    w.writeheader()
    for row in ImageData:
        #row = {k: v.encode('cp850','replace').decode('cp850') for k, v in row.items()}
        w.writerow(row)

with open(os.path.join(output_dir,"in_plutoF_not_GS.csv"), 'w', newline='', encoding="utf-8") as f:
    w = csv.DictWriter(f, NonMatchingSamplingEventData[0].keys())
    w.writeheader()
    for row in NonMatchingSamplingEventData:
        #row = {k: v.encode('cp850','replace').decode('cp850') for k, v in row.items()}
        w.writerow(row)
#cut the combined csv files to the ./Combined directory
for file in os.listdir(output_dir):
    if file.startswith("combined_"):
        #make the string of the file path to move
        #split the output_dir string on the os sep and pop the last element and rejoin the string by os.sep
        parent_folder = os.sep.join(output_dir.split(os.sep)[:-1])
        shutil.move(os.path.join(output_dir,file),os.path.join(parent_folder,"Combined",file))

## Addition of K on 10-01-2023 ##
#open AllAssociatedData.csv and write the data to it
outfile = os.path.join(output_dir,"AllAssociatedData_kme.csv")
data= pd.read_csv(os.path.join(output_dir,"AllAssociatedData.csv"),encoding='unicode_escape')
f = open(outfile,"w")
# turn the data into an array of rows (each element is a single row)
dataframein = data.to_numpy()
i=0
for row in dataframein:
    type = str(row[7])
    value = str(row[6]) 
    platefc = "NA"
    platenr = "NA"
    # find the pattern
    if type == "Image":
        sey = re.split(r"_(\d)([T,B])",value)
        if len(sey)==4:
            #print("--",sey[2],"--")
            platenr = str(sey[1]) # column "Plate Number"
            platefc = "Bottom" # column "Plate location"
            #print("--",sey[2],"--",platefc)
            if "T" in str(sey[2]): 
                platefc = "Top" 
            #print("--",sey[2],"--",platefc)
        else:
            platefc = "not provided"
            platenr = "not provided"
    f.write("{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],platefc,platenr,row[7],row[8],row[9],row[10]))
    i+=1
f.close()   

#delete the old AllAssociatedData.csv file
#rename the new AllAssociatedData_kme.csv file to AllAssociatedData.csv
os.remove(os.path.join(output_dir,"AllAssociatedData.csv"))
os.rename(os.path.join(output_dir,"AllAssociatedData_kme.csv"),os.path.join(output_dir,"AllAssociatedData.csv"))

