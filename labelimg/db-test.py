import images
import imagedb
import os
from PIL import Image
import imagehash
from imagedb import Dataset
import getpass
import time


password=getpass.getpass("Using login info: "+imagedb.login_info+"\nPASSWORD: ")
imagedb.connectDatabase(password)
images.buildFileTree(10000)

ids=os.listdir('web_ui_test')
folder='web_ui_test/'
images= [folder + image for image in ids]

print("Adding 10 images to database and file system from folder 'web_ui_test'")
i=0
while i<10:
	imagedb.addImage(images[i], 'test1', {})
	i+=1

print("\nImages added. Checking image integrity")
dataset=Dataset('test1')
while dataset.hasNext():
	data=dataset.getNext()
	print(data)
	hash=imagehash.average_hash(data[0])
	dbhash=data[1]['imagehash']
	if(str(hash)!=dbhash):
		message="\nIMAGES DO NOT MATCH!"
	else:
		message=" -Confirmed"
	print("Stored hash: "+str(hash)+" Database hash: "+str(dbhash)+message)
	
imagedb.db.newTag('test1', 'test')
print("\nNew tag created 'test1'")
print("\nTagging images with tag 'test1' and tag data {'test': 1}")
dataset=Dataset('test1')
while dataset.hasNext():
	print(dataset.getNext()[1])
	dataset.tag('test1', tag_data={'test': 1})

print("\nAdding 10 images into dataset test2")
while i<20:
	imagedb.addImage(images[i], 'test2', {})
	i+=1

imagedb.db.newTag('test2', 'test')
print("New tag created 'test2'")	
print("\nLoading and printing images in 'test2' without a tag (should be all 10), and tagging them with 'test2'")
dataset.loadUntagged({'dataset_name': 'test2'})
while dataset.hasNext():
	print(dataset.getNext()[1])
	dataset.tag('test2', tag_data={'test': 2})
	
print("test1 images have tag 'test1' and test2 images have tag test2")	
print("\nLoading and printing images without tag 'test2' and tagging them 'test2' (should be all images in dataset 'test1'")
dataset.loadUntagged({'tag_name': 'test2'})
while dataset.hasNext():
	print(dataset.getNext()[1])
	dataset.tag('test2', tag_data={'test': 2})
	
print("\nLoading and printing all images that haven't been tagged by 'test user2' (should be all 20)")
dataset.loadUntagged({'user_name': 'test user2'})
imagedb.db.user_id=imagedb.db.getUserID('test user2')
while dataset.hasNext():
	print(dataset.getNext()[1])
	dataset.tag('test1', tag_data={'test': 1})
	
print("\nLoading and printing all images that haven't been tagged by 'test user2' (should be none)")
dataset.loadUntagged({'user_name': 'test user2'})
while dataset.hasNext():
	print(dataset.getNext()[1])

	
	
"""BENCHMARKS.  *WILL CAUSE ERRORS IF NOT RUN PROPERLY	
import random	
print("Creating 10 temporary test datasets")
imagedb.newDataset('test1')
imagedb.newDataset('test2')
imagedb.newDataset('test3')
imagedb.newDataset('test4')
imagedb.newDataset('test5')
imagedb.newDataset('test6')
imagedb.newDataset('test7')
imagedb.newDataset('test8')
imagedb.newDataset('test9')
imagedb.newDataset('test10')
dataset_list=['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10']
tag_list=[]

rand_list=[]
for i in range(0, 50000):
	rand_list.append(random.randint(0, 9))
print("Inserting 50000 randomized image rows")
start=time.time()
for element in rand_list:
	temp_dataset=dataset_list[element]
	imagedb.db.insertImageRow(temp_dataset, imagehash=None)
end=time.time()
total_time=end-start
print("Operation time: "+str(total_time)+" seconds")
print("Selecting all images in set 1")
start=time.time()
imagedb.db.selectDataset('test1')
end=time.time()
total_time=end-start
print("Operation time: "+str(total_time)+" seconds")
print("Selecting all images in set 5")
start=time.time()
imagedb.db.selectDataset('test5')
end=time.time()
total_time=end-start
print("Operation time: "+str(total_time)+" seconds")

letters='abcdefghijklmnopqrstuvwxyz'
print("Inserting 1000 random tags")
for i in range (0, 1000):
	random_letter=random.choice(letters)
	imagedb.db.newTag(random_letter+str(i), 'test')
	tag_list.append(random_letter+str(i))
tag_data={'test': 1}
print("Randomly inserting 100000 tag links over first 50000 images")
start=time.time()
for i in range(0, 100000):
	imagedb.tagImage(random.randint(1,49999), tag_list[random.randint(0, 999)], tag_data=tag_data)
end=time.time()
total_time=end-start
print("Operation time: "+str(total_time)+" seconds")
print("Selecting all images tagged with "+tag_list[0])
start=time.time()
imagedb.db.selectWithTag(tag_list[0])
end=time.time()
total_time=end-start
print("Operation time: "+str(total_time)+" seconds")"""








	
	
