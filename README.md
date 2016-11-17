# HIIT-scripts
Scripts for my Funf project at HIIT.

## process_v2.py

The first step of getting readable data from the databases. It decrypts and compiles the databases into one big one, just like the original script, but this one allows more control over the process. Usage:

```
./process_v2.py <data dir> <password file>
```

where ```<data dir>``` is the directory where the databases to be processed are stored and ```<password file>``` is the file where the encryption password file is stored. This part of the process is completely functional.

## sqlite_process.py

This is a module used by ```convert_readable.py```. It handles the parsing of the data inside the data table that's inside the database file created by ```process_v2.py```; thus it should be kept in the same directory with ```convert_readable.py```.

## convert_readable.py

The script that converts the information from the database into coherent, readable information. Usage:

```
./convert_readable.py <database> <outfile>
```

where ```<database>``` is the database to be parsed and ```<outfile>``` is the output file for the processed info. Note that ```<outfile>``` can't exist as a directory nor a file, otherwise the script will exit without doing anything. NOTE: the converter doesn't completely work as of yet; time and package information are written as normal, but the location data doesn't appear. Kudos to Google's geolocation API for that.
