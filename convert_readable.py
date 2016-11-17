#!/usr/bin/env python3

from sys import argv
import os.path

import sqlite_process
import datetime
import http.client
import json

if len(argv) < 3:
	print(argv[0] + ": required args: <string database> <string outfile>")
	exit(0)

# database checks
dbase = os.path.abspath(argv[1])

if not os.path.isfile(dbase):
	print(argv[0] + ": invalid file:", argv[1])
	exit(0)

# outfile checks
ofile = os.path.abspath(argv[2])

if not os.path.isdir(os.path.dirname(ofile)):
	print(argv[0] + ": invalid file:", argv[2])
	exit(0)

if os.path.exists(ofile):
	print(argv[0] + ": file cannot exist")
	exit(0)

# probe checks
probelist = None
if len(argv) >= 4:
	probelist = argv[3].split(",")
	for probe in probelist:
		if not probe in probes.keys():
			print("no such probe:", probe)
			exit(0)

# probes:
probes = {
	"BatteryProbe": "edu.mit.media.funf.probe.builtin.BatteryProbe",
	"SmsProbe": "edu.mit.media.funf.probe.builtin.SmsProbe",
	"WifiProbe": "edu.mit.media.funf.probe.builtin.WifiProbe",
	"SimpleLocationProbe": "edu.mit.media.funf.probe.builtin.SimpleLocationProbe",
	"ProcessStatisticsProbe": "edu.mit.media.funf.probe.builtin.ProcessStatisticsProbe",
	"TelephonyProbe": "edu.mit.media.funf.probe.builtin.TelephonyProbe",
	"ContactProbe": "edu.mit.media.funf.probe.builtin.ContactProbe",
	"ApplicationsProbe": "edu.mit.media.funf.probe.builtin.ApplicationsProbe",
	"ServicesProbe": "edu.mit.media.funf.probe.builtin.ServicesProbe",
	"CallLogProbe": "edu.mit.media.funf.probe.builtin.CallLogProbe",
	"HardwareInfoProbe": "edu.mit.media.funf.probe.builtin.HardwareInfoProbe",
	"AccountsProbe": "edu.mit.media.funf.probe.builtin.AccountsProbe",
	"RunningApplicationsProbe": "edu.mit.media.funf.probe.builtin.RunningApplicationsProbe",
	"ScreenProbe": "edu.mit.media.funf.probe.builtin.ScreenProbe"
}

probe_allow = [probes["RunningApplicationsProbe"]]

if probelist:
	for i in range(len(probelist) - 1):
		probelist[i] = probes[probelist[i]]

	probe_allow = probelist

# functions
def checknight(timestamp):
	# True = night
	# False = day

	time = datetime.datetime.fromtimestamp(timestamp).hour

	return 21 <= time <= 9

def formatd(duration):
	dtime = datetime.datetime.fromtimestamp(duration)
	hours = dtime.hour
	minutes = dtime.minute
	seconds = dtime.second

	return str(hours) + "h " + str(minutes) + "m " + str(seconds) + "s"

def getaddrfromcoords(lat, lon):
	apiconn = http.client.HTTPSConnection("https://maps.googleapis.com")
	apiconn.request("GET", "/maps/api/geocode/json?latlng=" + lat + "," + lon + "&key=AIzaSyAsvKel-_ZPC0Bsep1HllGACDdAvoBYBdM")
	parsed_res = json.loads(apiconn.getresponse())
	apiconn.close()

	for dictionary in parsed_res["results"]["address_components"]:
		if "street_number" in dictionary["types"]:
			addr_strt = dictionary["long_name"]
		elif "route" in dictionary["types"]:
			addr_rdnm = dictionary["long_name"]
		elif "administrative_area_level_1" in dictionary["types"]:
			addr_city = dictionary["long_name"]
		elif "country" in dictionary["types"]:
			addr_cntr = dictionary["long_name"]

	return [addr_rdnm + " " + addr_strt + ", " + addr_city + ", " + addr_cntr, parsed_res["results"]["status"]]

def parse2file(database, outfile):
	tformat = "%d.%m.%Y %H:%M:%S"
	with open(outfile, "w") as fl:
		for dentry in sqlite_process.tableparser(database):
			entries = dict()

			datadict = dentry.value

			locprobe = None
			if dentry.probe == probes["SimpleLocationProbe"]:
				locprobe = {"latitude": dentry.value["mLatitude"], "longitude": dentry.value["mLongitude"]}
			if dentry.probe in probe_allow and checknight(dentry.timestamp) == False:
				datadict = dentry.value
				for key in datadict.keys():
					if key == "taskInfo":
						tinfo = datadict[key]
						fl.write(tinfo["baseActivity"]["mPackage"] + "\t")
						fl.write(datetime.datetime.fromtimestamp(tinfo["lastActiveTime"] / 1000).strftime("%H:%M") + " - " + datetime.datetime.fromtimestamp((tinfo["lastActiveTime"] + datadict["duration"] * 1000) / 1000).strftime("%H:%M") + "\t")
						
						if locprobe:
							loc = getaddrfromcoords(locprobe["latitude"], logprobe["longitude"])
							if loc[1] == "OK":
								fl.write(loc[0] + "\n")
							else:
								fl.write(str(loc[1]) + "\n")

				fl.write("\n")

parse2file(dbase, ofile)
