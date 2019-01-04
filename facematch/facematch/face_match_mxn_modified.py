import tensorflow as tf
import numpy as np
import facenet
from align import detect_face
#import detect_face
import cv2
import argparse
import os
import pandas as pd
import datetime
a = datetime.datetime.now()

parser = argparse.ArgumentParser()
parser.add_argument("--db", type = str, required=True)
args = parser.parse_args()

####################################################
'''
import os
from pdf2image import convert_from_path
#rootdir = '/home/cso/Downloads/customer_pdfs'

for subdir, dirs, files in os.walk(args.db):
	for file in files:
		full_path = os.path.join(subdir, file)
		if full_path.endswith('.pdf'):
			converted_name = os.path.join(subdir, '%s_conv.jpg' % (file.replace('.pdf', '')))
			#converted_name_2 = os.path.join(subdir, '%s_conv_2.jpg' % (file.replace('.pdf', '')))
			images = convert_from_path(full_path,500,output_folder=subdir,fmt='jpg', first_page=1, last_page=1)
			#images2 = convert_from_path(full_path,500,output_folder=subdir,fmt='jpg', first_page=9, last_page=9)
			os.rename(images[0].filename, converted_name)
			#os.rename(images2[0].filename, converted_name_2)

'''
###################################################



# some constants kept as default from facenet
minsize = 20
threshold = [0.6, 0.7, 0.7]
factor = 0.709
margin = 44
input_image_size = 160

sess = tf.Session()

# read pnet, rnet, onet models from align directory and files are det1.npy, det2.npy, det3.npy
pnet, rnet, onet = detect_face.create_mtcnn(sess, 'align')

# read 20170512-110547 model file downloaded from https://drive.google.com/file/d/0B5MzpY9kBtDVZ2RpVDYwWmxoSUk
facenet.load_model("20170512-110547/20170512-110547.pb")

# Get input and output tensors
images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
embedding_size = embeddings.get_shape()[1]

def getFace(img):
    faces = []
    img_size = np.asarray(img.shape)[0:2]
    bounding_boxes, _ = detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
    if not len(bounding_boxes) == 0:
        for face in bounding_boxes:
            if face[4] > 0.50:
                det = np.squeeze(face[0:4])
                bb = np.zeros(4, dtype=np.int32)
                bb[0] = np.maximum(det[0] - margin / 2, 0)
                bb[1] = np.maximum(det[1] - margin / 2, 0)
                bb[2] = np.minimum(det[2] + margin / 2, img_size[1])
                bb[3] = np.minimum(det[3] + margin / 2, img_size[0])
                cropped = img[bb[1]:bb[3], bb[0]:bb[2], :]
                resized = cv2.resize(cropped, (input_image_size,input_image_size),interpolation=cv2.INTER_CUBIC)
                prewhitened = facenet.prewhiten(resized)
                faces.append({'face':resized,'rect':[bb[0],bb[1],bb[2],bb[3]],'embedding':getEmbedding(prewhitened)})
    return faces

def getEmbedding(resized):
    reshaped = resized.reshape(-1,input_image_size,input_image_size,3)
    feed_dict = {images_placeholder: reshaped, phase_train_placeholder: False}
    embedding = sess.run(embeddings, feed_dict=feed_dict)
    return embedding

bad_images = []
file_embedding_dict = {}
for subdir, dirs, files in os.walk(args.db):
	for file in files:
		full_path = os.path.join(subdir, file)
		if full_path.endswith(('.jpg','.Jpg','.jpeg','.png')):
			img2 = cv2.imread(full_path)
			face1 = getFace(img2)
			try:
				file_embedding_dict[file] = face1[0]['embedding']
			except:
				print(full_path)
				bad_images.append(full_path)

#print("file_embedding_dict", file_embedding_dict)


def compare2multiple(embed_dict):
	#threshold = 0.74    # set yourself to meet your requirement 
	threshold = 0.54
	compare_result_dict = {}
	dist_list = []
	count = 0
	for kf1, vf1 in embed_dict.items():
		compare_result_dict[kf1] = []
		for kf2, vf2 in embed_dict.items():
			dist = np.sqrt(np.sum(np.square(np.subtract(vf1, vf2))))
			count = count + 1
			if dist <= threshold:
				similarity = "%.2f" % (1 / (1 + dist) * 100)
				if float(similarity) < 100:
					compare_result_dict[kf1].append(kf2)
					compare_result_dict[kf1].append(str(similarity))
	print (count)
	return compare_result_dict, count

d,count = compare2multiple(file_embedding_dict)

print("compare result: ", d)

df = pd.DataFrame(list(d.items()), columns = ['sourceImage', 'matchingImages'])
df['matchingImages'] = df['matchingImages'].astype('str')
df['matchingImages'] = df['matchingImages'].apply(lambda x: x.strip('[]'))
df['matchingImages'] = df['matchingImages'].apply(lambda x: "".join(x.split("'")))

print(df.head())
		
df.to_csv("/home/cso/facematch/output/facematch_new_all_applications.csv")


############### SQL #########################
from sqlalchemy import create_engine 
import urllib
server = '*******'
database = '*******'
username = '*******'
password = '*******'
#driver='{ODBC Driver 17 for SQL Server}'
#Enabled = 'Enabled'
params = urllib.parse.quote_plus(
'DRIVER={ODBC Driver 17 for SQL Server};'+ 
'SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password) 

engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params) 
pd.io.sql._is_sqlalchemy_connectable(engine)


df.to_sql('FDS2', con=engine, if_exists='append', index=False, chunksize=20000) 
#################################################

b = datetime.datetime.now()

print (b)

c = b - a

print(bad_images)
print ("Total iterations:",count)
time = divmod(c.days * 86400 + c.seconds, 60)
print ("Execution time:",time)
