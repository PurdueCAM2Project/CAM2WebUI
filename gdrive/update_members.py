#############################
# Member Picture Updating Script
#
# Execute "python -m gdrive.update_members" to run this script.
#
# NOTE: Needs modification before it is possible to correctly run.
# You mostly need to change the constants below to update the subteams,
# although it might be necessary to change some of the for loops if the
# format of the spreadsheets change. For these loops, look for the word
# "NOTE".
#############################

# Location to save the backup of the current member picture data
OLD_MEMBER_FILE = "members_old.json"

# Files to read the picture and subteam data from
SUBTEAM_FILE = '../2019SpringTeams - Sheet1.csv'
MEMBER_FILE = '../CAM2 Member Information.csv'

# People who want their name changed
RENAME_PEOPLE = {'Nathan Gizaw|Drone Video': 'Nathan M. Gizaw','Paul Chang|Human Behavior in Video':'Paul B. Zhang','Andrew Shen|Forest Inventory Analysis':'Yezhi Shen'}

# Lift of people to be marked as leaders
LEADERS = ['Ling Zhang', 'Damini Rijhwani', 'Noureldin Hendy', 'Noah Curran', 'Alex Xu', 'Matthew Kelleher', 'Andrew Shen', 'Paul B. Zhang', 'Rohan Prabhu', 'Mohamad Alani', 'Anirudh Vegesana', 'Nathan M. Gizaw', 'Sripath Mishra', 'Krishna Kumar', 'Daniel Merrick', 'Karthik Maiya', 'Ashley Kim', 'Xiao Hu', 'Ryan Dailey']

# Descriptions of new subteams
SUBTEAM_DESCRIPTIONS = {'Technology Commercialization': 'Enter into the Burton D. Morgan Business Model Competition.', 'Adaptive Object Detection': 'Our team is focused on developing adaptive object detection software that improves object detection on night time image data.', 'Parallel Computing for Vision': 'Use camera parameters (time of the day, location) to increase the confidence of object detection in real time analysis.', 'Dataset Bias': 'Improve the performance of transfer learning by utilizing how the concentration of objects of interest in training data change how well the model transfers to a new dataset with objects of interest concentrated in a different region.', 'Camera Discovery + Reliability': 'Find factors to identify useful cameras for emergency responses.', 'Crowdsourcing': 'Reduce the biased results in incorrectly trained image processing classifiers by utilizing the power of crowdsourcing. ', 'Human Behavior in Video': 'To detect and map pedestrian traffic in targeted areas for land development through consistent re-identification. The data for analysis will be collected through twenty-four hour live feeds.', 'Web UI + Camera API': 'Maintain, update and improve the content and user interface at cam2project.net. Build the new website for helps site. Ensure easily accessibility of the camera database. Ensure the correctness of data in the database.', 'Graduate Students': ''}

# Rename existing subteams to new ones. Renaming a defunct team to a new team is fine.
RENAME_SUBTEAMS = {'Camera Discovery + Reliability': 'Camera Reliability', 'Crowdsourcing': 'WebUI', 'Human Behavior in Video': 'Human Behavior', 'Web UI + Camera API': 'Camera Database API and Discovery', 'Parallel Computing for Vision': 'Embedded Vision', 'Adaptive Object Detection': 'Context-Based Vision', 'Technology Commercialization': 'Transfer Learning'}

# List of Simpson family members to choose a picture from if someone doesn't upload their picture
SIMPSONS = ['https://pbs.twimg.com/profile_images/609439993094770690/MqfzEbtj_400x400.jpg', 'https://img.discogs.com/-Rva9vDUKpsFCLpVgZcbfOGTGiU=/300x300/smart/filters:strip_icc():format(jpeg):mode_rgb():quality(40)/discogs-images/A-1010823-1335728016.png.jpg', 'http://icons.iconarchive.com/icons/jonathan-rey/simpsons/256/Lisa-Simpson-icon.png', 'https://www.google.com/url?sa=i&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwjz-PaOxZbgAhVk04MKHZUSAj0QjRx6BAgBEAU&url=http%3A%2F%2Fcharacters.wikia.com%2Fwiki%2FMaggie_Simpson&psig=AOvVaw1f6mqqF8zZicpxEpftRvaA&ust=1548973234004880', 'https://vignette.wikia.nocookie.net/characters/images/9/9d/Maggie_Simpson.png/revision/latest?cb=20170823025740' 'http://averagejaneruns.com/wp-content/uploads/2011/11/exhausted-marge.gif']

import django
import os

# Start up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cam2webui.settings")
django.setup()

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from app import models
from collections import defaultdict
import csv
import random

# Save old members
if OLD_MEMBER_FILE:
	data = serializers.serialize("json", list(models.Subteam.objects.all()) + list(models.TeamMember.objects.all()))
	out = open(OLD_MEMBER_FILE, "w")
	out.write(data)
	out.close()

# Find out who is new and who is not
subteams = dict()
isNew = dict()
with open(SUBTEAM_FILE, newline='') as csvfile:
	reader = csv.reader(csvfile)
	next(reader, None) # Skip headers
	
	# NOTE: Change this line if the layout of the spreadsheets change
	for team, time, leader, first, last, email, major, credit, met, VIP, graduation, new, course in reader:
		subteams[first+' '+last] = team.strip()
		isNew[first+' '+last] = new

# Get photos for each member
photos = defaultdict(dict)
with open(MEMBER_FILE, newline='') as csvfile:
	reader = csv.reader(csvfile)
	next(reader, None) # Skip headers
	
	# NOTE: Change this line if the layout of the spreadsheets change
	for timestamp,first,last,email,name,gitHub,crn,extPhot,photo,linkedIn,gpu in reader:
		if extPhot and extPhot.startswith('http'):
			photo = extPhot
		elif photo:
			photo = 'https://drive.google.com/uc?id='+photo.split('id=')[1]
		else:
			photo = random.choice(SIMPSONS)
		name = first.strip() + ' ' + last.strip()
		
		success = False
		try:
			subteam = subteams[name]
			success = True
		except KeyError:
			subteam = input(name+": ").strip()
		
		photos[subteam][name] = photo

# You can hardcode the data here to make manual modifications
#photos = defaultdict(dict, {'Camera Discovery + Reliability': {'Sripath Mishra': 'https://docs.google.com/uc?id=1VBRo4-fnfTBJez8oG-z1_dCdOtRizcs2', ...}})

# Manually correct the data
if RENAME_PEOPLE:
	for old_key, new_key in RENAME_PEOPLE.items():
		name, team = old_key.split('|')
		photos[team][new_key] = photos[team].pop(name)
if RENAME_SUBTEAMS:
	for new_key, old_key in RENAME_SUBTEAMS.items():
		try:
			subteam = models.Subteam.objects.get(name=old_key)
			subteam.name = new_key
			subteam.save()
		except ObjectDoesNotExist:
			print(old_key + " already renamed.")

# Create new subteams
for name, desc in subteams.items():
	try:
		subteam = models.Subteam.objects.get(name=name)
		subteam.description = desc
		subteam.save()
	except ObjectDoesNotExist:
		subteam = models.Subteam.objects.create(name=name, description=desc)
		print(name + " created.")

# Remove all old members and add all of the new members to their new teams
# For all new members, this prints out if they are considered new in the spreadsheet. You should check these values before you run it on production
models.TeamMember.objects.all().update(iscurrentmember=False)
subteams = {team.name: team for team in models.Subteam.objects.all()}
rename_people_reversed = {v: k for k, v in RENAME_PEOPLE.items()}
for team, s in photos.items():
	for name, photo in s.items():
		try:
			member = models.TeamMember.objects.get(name=name)
			member.subteam = subteams[team]
			member.iscurrentmember = True
			member.image_url = photo
			member.isdirector = name in leader
			if name in rename_people_reversed:
				nameNew, newTeam = rename_people_reversed[name].split('|')
				member.name = nameNew
			member.save()
		except ObjectDoesNotExist:
			member = models.TeamMember.objects.create(name=name, subteam=subteams[team], iscurrentmember=True, image_url=photo, isdirector = name in leader)
			try:
				print(name + " is new: " + isNew[name])
			except:
				print(name + " is new: !")
