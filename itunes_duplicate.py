#This is from a coding book: "Python Playground: Geeky Projects for the Curious Programmer".

#I filled in some of my own comments to help me really understand what we were doing.  
#I also added the Artist name to the output for duplicate song.
#I highly recommend buying this fun, project-based book:  
#http://www.amazon.com/Python-Playground-Projects-Curious-Programmer-ebook/dp/B017AH8H7I/ref=mt_kindle?_encoding=UTF8&me=

import re, argparse
import sys
from matplotlib import pyplot
import plistlib
import numpy as np





#- - - - - GETFILE/MAKETRACKLIST+NAMES+LENGTH+COUNT/ - - - - - - - - - - - - - 
#- - - - - CYCLEFULLTRACKLIST+ADDNAMES+LENGTH+COUNT>EMPTY TRACKLIST- - - - - - - - - - - - - 



# declaring method name and argument that are clues to what method does
def findDuplicates(fileName):
	#GETFILE
	#letting user know what this method does
	print('Finding duplicate tracks in %s...' % fileName)
	# importing playlist dictionary structure and setting it equal to plist using plistlib library
	plist = plistlib.readPlist(fileName)
	# pulls track name from playlist dictionary MAKING FULL TRACK NAMES DICTIONARY
	tracks = plist['Tracks']
	#MAKETRACKLIST
	#Make EMPTY tracklist+NAME+LENGTH+COUNT
	#create an empty track name dictionary that will keep track of duplicates
	trackNames = {}
	#Cycle FULL tracklist dictionary (still don't know why trackID & track are indicated)
	for trackId, track in tracks.items():
		try:
			#PULL NAME and DURATION for each track from the FULL tracklist
			name = track['Name']
			artist = track['Artist']
			duration = track['Total Time']
			#look for existing entries in EMPTY tracklist
			#Look for matches in NAME
			if name in trackNames:
				#look for matches in DURATION
				#round the track length to the nearest second
				if duration//1000 == trackNames[name][0]//1000:
					#if there is a match with both DURATION/NAME set COUNT to 
					#what is the 2nd value for EMPTY tracklist key
					count = trackNames[name][1]
					#ADDNAMES+LENGTH+COUNT>EMPTY TRACKLIST
					#if a name and duration match, set it equal to track duration and increment the count 1 
					trackNames[name] = (duration, count+1, artist)
			else:
				#add dictionary entry as tuple (duration, count)
				trackNames[name] = (duration, 1, artist)
		except:
			#ignore
			pass
			
			
		
			
	#iterate through the tracks (still don't know why trackID & track are indicated instead of just one)



#- - - - - - - - - - - - - -EXTRACTING DUPLICATES - - - - - - - - - - - - - - - - 
# So we are extracting from a no long EMPTY tracklist: trackNames = {}
# trackNames structure = {key(Track Name):  duration[0], count[1]}
# store duplicates as (name, count) tuples
# dups is where we will keep a list of duplicate tracks
	dups = []
#Cycle through trackNames and pull two items (k, v) > generic assignments
	for k, v in trackNames.items():
		#If count is > 1
		if v[1] > 1:
			#Add COUNT (v[1]) and NAME(k...is key....k[0]would make it DURATION which we don't want)
			dups.append((v[1], k, v[2]))
	# save DUPLICATES to separate .TXT file
	#If any duplicates are found
	if len(dups) > 0:
	#Tell user how many duplicates were found and where we are writing them
		print('Found %d duplicates.  Track names saved to dup.txt' % len(dups))
	#or
	else:
		#tell user that there are no duplicates
		print('No duplicate tracks found!')
	#create a new document > open it and make it writable ('w')
	f = open('dups.txt', 'w')
	#cycle through duplicates list over each key
	for val in dups:
		#write to dups.txt file COUNT(val[0]) and NAME(val[1])
		f.write('[%d] %s - %s\n' % (val[0], val[1], val[2]))
	#After it is finished, close the txtfile	
	f.close()

#- - - - - - - - - - FINDING TRACKS COMMON ACROSS MULTIPLE PLAYLISTS - - - - - - - - - -  - 

#pass list of .xml files to findCommonTracks
def findCommonTracks(fileNames):
	# a list of sets of track names
	trackNameSets = []
	#for each .xml file
	for fileName in fileNames:
		#create a new set
		trackNames = set()
		#read in playlist fore each .xml file
		plist = plistlib.readPlist(fileName)
		#get the tracks from .xml file
		tracks = plist['Tracks']
		#iterate through the tracks
		for trackId, track in tracks.items():
			try:
				#add the track name to a set
				trackNames.add(track['Name'])
			except:
				#ignore
				pass
			#add individual track list set to sets list
		trackNameSets.append(trackNames)
	# get the set of common tracks
	commonTracks = set.intersection(*trackNameSets)
	# write tracks to file
	if len(commonTracks) > 0:
		f = open('common.txt', 'w')
		for val in commonTracks:
			s = '%s\n' % val
			f.write(s.encode('UTF 8'))
		f.close()
		print('%d common tracks found. '
				'Track names written to common.txt.' % len(commonTracks))
	else:
		print('No common tracks!')
		
		
		
#- - - - - - - - - - - - - - - - COLLECTING STATS-  -- - - - - - - - - - - - - - - 

def plotStats(fileName):
	#read in the .xml file
	plist = plistlib.readPlist(fileName)
	# get the tracks from the playlist
	tracks = plist['Tracks']
	# create lists of song ratings and track durations
	ratings = []
	durations =[]
	#iterate through the track list
	for trackId, track in tracks.items():
		try:
			ratings.append(track['Album Rating'])
			durations.append(track['Total Time'])
		except:
			#ignore
			pass
	#ensure that valid data was collected
	if ratings == [] or durations == []:
		print('No valid Album Rating/Total Time data in %s.' % fileName)
		return


#- - - - - - - - - - - - - - - - PLOTTING STATS - - - - - - - - - - - - - - 

	#scatter plot
	x = np.array(durations, np.int32)
	#convert to minutes
	x = x/60000.0
	y = np.array(ratings, np.int32)
	pyplot.subplot(2,1,1)
	pyplot.plot(x,y, 'o')
	pyplot.axis([0, 1.05 *np.max(x), -1, 110])
	pyplot.xlabel('Track duration')
	pyplot.ylabel('Track rating')
	
	#plot historgram
	pyplot.subplot(2, 1, 2)
	pyplot.hist(x, bins=20)
	pyplot.xlabel('Track duration')
	pyplot.ylabel('Count')
	
	#show plot
	pyplot.show()
	
	
#- - - - - - - - - - - - -COMMAND LINE - - - - - - - - - - - - - 


def main():
	# create parser
	descStr = '''
	This program analyzes iTunes playlist files (.xml).'''
	
	parser = argparse.ArgumentParser(description=descStr, add_help=False)
	#add mutually exclusive group of arguments
	group = parser.add_mutually_exclusive_group()
	
	#add expected arguments
	group .add_argument('--common', nargs = '*', dest='plFiles', required=False)
	group .add_argument('--stats', dest = 'plFile', required=False)
	group .add_argument('--dup', dest = 'plFileD', required=False)
	
	#parse args
	args = parser.parse_args()
	
	if args.plFiles:
		#find common tracks
		findCommonTracks(args.plFiles)
	elif args.plFile:
		#plot stats
		plotStats(args.plFile)
	elif args.plFileD:
		#find duplicates
		findDuplicates(args.plFileD)
	else:
		print("These are not the tracks you are looking for.")

# main method
if __name__ == '__main__':
	main()