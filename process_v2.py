#!/usr/bin/python

import os.path
import inspect
import sys
import glob

if len(sys.argv) < 3:
	print("Usage: " + sys.argv[0] + " <db directory> <encryption key file>")
	exit(0)

if not os.path.isdir(sys.argv[1]):
	print(sys.argv[0] + ": not a directory: " + sys.argv[1])
	exit(0)

if not os.path.isfile(sys.argv[2]):
	print(sys.argv[0] + ": not a file " + sys.argv[2])
	exit(0)

raw_data_dir = os.path.abspath(sys.argv[1])
data_dir = os.path.dirname(raw_data_dir)
password_file = os.path.abspath(sys.argv[2])
script_dir = os.path.join(os.path.dirname(data_dir), "scripts/raw_scripts/scripts")
merged_data_file = os.path.join(data_dir, 'all_data.db')
data_processing_scripts_dir = os.path.join(script_dir, 'data_processing')
processing_file = os.path.join(data_dir, "process")
merged_data_file = os.path.join(data_dir, "all_data.db")

sys.path.append(data_processing_scripts_dir)
import dbdecrypt
import dbmerge
import decrypt
import shutil

def process_data():
    # load decrypt password
    with open(password_file, 'r') as file:
        encryption_password = file.read().split("\n")[0]
    encryption_key = decrypt.key_from_password(encryption_password)
    
    # dbDecrypt all files in raw
    db_files = glob.glob(os.path.join(raw_data_dir, '*.db'))
    failed_files = []
    for fl in db_files:
    	if not dbdecrypt.decrypt_if_not_db_file(fl, encryption_key):
	    failed_files.append(fl)

    # merge all files in raw
    decrypted_files = list(set(db_files) - set(failed_files))
    dbmerge.merge(db_files=decrypted_files, out_file=processing_file, overwrite=True, attempt_salvage=True)
    
    
    # replace current file
    shutil.move(processing_file, merged_data_file)
    
    # TODO: add data report

if __name__ == "__main__":
    process_data()
