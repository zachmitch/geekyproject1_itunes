#This is from a coding book: "Python Playground: Geeky Projects for the Curious Programmer".

#I filled in some of my own comments to help me really understand what we were doing.  
#I also added the Artist name to the output for duplicate song.
#I highly recommend buying this fun, project-based book:  
#http://www.amazon.com/Python-Playground-Projects-Curious-Programmer-ebook/dp/B017AH8H7I/ref=mt_kindle?_encoding=UTF8&me=

import plistlib




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


def findCommonTracks(fileNames):
	# a list of sets of track names
	trackNameSets = []
	for fileName in fileNames:
		#create a new set
		trackNames = set()
		#read in playlist
		plist = plistlib.readPlist(fileName)
		#get the tracks
		tracks = plist['Tracks']
		#iterate through the tracks
		for trackId, track in tracks.items():
			try:
				#add the track name to a set
				trackNames.add(track['Name'])
			except:
				#ignore
				pass
			#add to list
		trackNameSets.append(trackNames)
	# get the set of common tracks
	commonTracks = set.intersection(*trackNameSets)
	# write to file
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
