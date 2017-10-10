import db
import images
from PIL import Image
import imagehash
import json
from db import DB

db=DB()
login_info="host: 128.46.213.21, user_type: cam2team,  db_name: ImageDBTest, user_name: test user1"

def connectDatabase(password, host='128.46.213.21', user_type='cam2team',  db_name='ImageDBTest', user_name='test user1'):
	#Connecting to database.  Essential function
	db.connect(host, user_type, db_name, user_name, password)
	
def newDataset(name, num_images=0):
	#Every image must reference a dataset
	db.insertDatasetRow(name)
	
def addImage(image_path, dataset_name='test', image_dict={}):
	#Add image metadata to database and image to file system
	image_dict['dataset_name']=dataset_name
	im=Image.open(image_path)
	image_hash=imagehash.average_hash(im)
	if(db.hasImage(image_hash)):
		print("Image already exists in database")
		return 
	x_resolution, y_resolution=im.size
	image_dict['x_resolution']=x_resolution
	image_dict['y_resolution']=y_resolution
	image_dict['imagehash']=image_hash
	db.insertImageRow(**image_dict)
	images.addJpeg(im, db.getLastID())
	   
def tagImage(image_id, tag_name, tag_data={}):
	#Insert a tag link into database
	tag_id=db.getTagID(tag_name)
	if tag_id is None:
		db.newTag(tag_name)
	tag_id=db.getTagID(tag_name)
	json_string=None
	if tag_data:
		json_string=json.dumps(tag_data)
	db.insertTagLink(tag_id, image_id, tag_data=json_string) 
	
class  Dataset():
	#psuedo singly linked list
	#This class should be used to quickly tag images.
	#Recommend directly accessing the rows list to dynamically access data
	#
	def __init__(self, dataset_name=None):
		if not db.connected:
			print("You are not connected.")
			return
		if dataset_name is not None: #alternatively call 'loadUntagged' after initializing 
			self.rows=db.selectDataset(dataset_name)
		self.current_image=()
		
	def loadUntagged(self, parameters={}):
		#Loading untagged images fitting <parameters>.  See db.py for parameter options
		#if parameters is not passed, then all untagged images will be loaded
		self.rows=db.selectUntagged(**parameters)
		
	def getNext(self):
		if self.rows:
			row=self.rows.pop()
			pil_image=images.getJpeg(row['id'])
			self.current_image=(pil_image, row)
			return self.current_image
		return 0
	
	def tag(self, tag_name, tag_data=None):
		#Tagging 'self.current_image'
		image_id=self.current_image[1]['id']
		json_string=json.dumps(tag_data)
		tagImage(image_id, tag_name, json_string)
		
	def hasNext(self):
		return self.rows
