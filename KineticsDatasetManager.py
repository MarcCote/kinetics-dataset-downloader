"""
MIT License

Copyright (c) 2019 Rockson Agyeman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
Author:		Rockson Agyeman and Gyu Sang Choi
Date: 		2019.05.27
Email:		rocksyne@gmail.com, castchoi@ynu.ac.kr
Version:	1.0.0
Purpose:	Manage kinetics dataset according to author guidelines

* Download dataset from https://deepmind.com/research/open-source/open-source-datasets/kinetics/


REFS:
https://www.ostechnix.com/20-ffmpeg-commands-beginners/
"""


# import the libraries we need
import os, sys
from tqdm import tqdm as tqdm
import shutil
from pytube import YouTube


# Class begins
class KineticsDatasetManager(object):

	# constructor
	def __init__(self,destination_path=None,dataset_type=None):
		
		self.destination_path = destination_path
		self.dataset_type = str(dataset_type).lower()

		# the dataset type can never be empty
		if self.dataset_type is None:
			sys.exit("Please provide the category of dataset [train,validate,test] ")


		# we need to make sure that the destination path really exists
		# if it doesnt, we will need to create a temp one in this current working dir
		if self.destination_path is None:
			self.destination_path = os.path.join(os.getcwd(),"Kinetics_dataset",str(dataset_type))
			print("")
			print("Destination directory defaulted to '",self.destination_path,"'")
			print("")

		else: self.destination_path = os.path.join(self.destination_path,str(dataset_type))


		# chek if destination exists. if it does, delete and create new one
		if os.path.exists(self.destination_path):
			print("")
			print("Destination path '{}' already exists. Deleting and re-creating...".format(self.destination_path))
			print("")
			shutil.rmtree(self.destination_path)
			os.makedirs(self.destination_path)

		else:
			os.makedirs(self.destination_path)
			print("")
			print("Destination path '{}' created successfully!".format(self.destination_path))
			print("")
	



	# return the list of all split files in the dir that
	# that matches the split version number
	"""
		This code will need some working on. For now we are not able to download only a component the youtube datase
		So what we shall do is, download each video and use post processing to crop out the part of the video we need
		Thats just the hard way out for now

		-- To do --
		[ref: https://github.com/ytdl-org/youtube-dl/issues/622#issuecomment-162337869]
	"""
	def download_video(self):

		if self.dataset_type == "train":
			csv_location = "./dataset_splits/kinetics_600/kinetics_train.csv"

		elif self.dataset_type == "validate":
			csv_location = "./dataset_splits/kinetics_600/kinetics_val.csv"

		elif self.dataset_type == "test":
			csv_location = "./dataset_splits/kinetics_600/kinetics_600_test.csv"

		elif self.dataset_type == "holdout":
			csv_location = "./dataset_splits/kinetics_600/kinetics_600_holdout_test.csv"

		else:
			sys.exit("Invalid dataset category type. Please enter [train,validate,test]")


		#number may not be right but just give us a rough estimate	
		video_counter = 0

		# open the file
		with open(csv_location,"r") as opened_csv:
			lines = opened_csv.readlines()
			lines = [line.rstrip('\n') for line in lines]

			# since the first line is just headings,
			# we will chop that part off
			lines = lines[1:]
			sp = "./"

			# loop through the lines to downlad the video
			for line in tqdm(lines):
				coumn = str(line).split(",")

				# there is no label for holdout data
				if self.dataset_type == "holdout":
					data_lable = "all_data"
					youtube_id = coumn[0]
					start_time = coumn[1]

				else:
					data_lable = coumn[0]
					youtube_id = coumn[1]
					start_time = coumn[2]
					

				# create the directory according to the label name
				dir_name = str(data_lable).replace(" ","_") # replace space with underscore
				dir_name = os.path.join(self.destination_path,dir_name) # make it an absolute path

				# if the directory does not already exist
				# then create a new one
				if os.path.exists(dir_name) is False:
					os.makedirs(dir_name)

				# sample video name
				vid_name = "vid_"+youtube_id+".avi"
				vid_path = os.path.join(dir_name,vid_name)

				# create the youtube link
				youtube_link = "https://www.youtube.com/watch?v="+youtube_id

				# use youtube-dl and ffmpeg to download videos
				os.system("ffmpeg -hide_banner -ss "+start_time+" -i $(youtube-dl -f 18 --get-url "+youtube_link+") -t 10 -c:v copy -c:a copy "+vid_path)
				video_counter +=1
				print(video_counter, " videos download")
