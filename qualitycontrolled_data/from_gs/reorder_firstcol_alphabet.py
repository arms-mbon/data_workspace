#this script will reorder the first column of a csv file alphabetically
import os
#get the directory where the files are located
script_dir = os.path.dirname(__file__)
folder_to_check = script_dir
file_prefix = "GS_ARMS_"

#get all files in the folder that start with the prefix
files = [f for f in os.listdir(folder_to_check) if f.startswith(file_prefix)]

#go through each file and reorder the first column alphabetically
for file in files:
    with open(os.path.join(script_dir, file), 'r') as f:
        lines = f.readlines()
        #take out the first line
        header = lines.pop(0)
        lines.sort()
        with open(os.path.join(script_dir, file), 'w') as f:
            f.write(header)
            for line in lines:
                f.write(line)