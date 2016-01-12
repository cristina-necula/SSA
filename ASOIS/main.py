import dropbox
import datetime
import os
import sys
import time
from os.path import basename
from dropbox.files import FileMetadata, FolderMetadata

TOKEN = 'NLGoIVvvLnkAAAAAAAAAMt84FzFhQpSo_OyKurzkFatXgFKvFv2IOeNEj-HUP13v'
LOCAL_PATH = ""
UPLOAD_PATH = "/" + LOCAL_PATH
MB = 1000000

def configure_dropbox():
	""" Configure Dropbox account
	"""
	try:
		dbx = dropbox.Dropbox(TOKEN)
		print 'Linked Dropbox account: ', dbx.users_get_current_account().email
	except dropbox.exceptions.BadInputError as err:
		print 'Instantiating Dropbox instance failed with error: '
		print err

	return dbx	

def generate_files():

	if not os.path.exists(LOCAL_PATH):
		os.makedirs(LOCAL_PATH)

	nr_of_files = 11
	for i in range(1, nr_of_files):
		file_name = LOCAL_PATH + '/file_' + str(i)
		with open(file_name, 'wb') as fout:
			fout.write(os.urandom(i * sys.maxsize / 150))

def download_file(dbx, file_name):
	
	file_path = '%s/%s' % (UPLOAD_PATH, file_name)
	start_time = time.time()
	try:
		md, res = dbx.files_download(file_path)
		end_time = time.time()
		data = res.content
		print("Downloading %.2f MB in %.3fs" % 
			(len(data) * 1.0 / MB, end_time - start_time))
	except dropbox.exceptions.ApiError as err:
		print 'Error downloading file'
		print err

def upload_file(dbx, file_name):
	
	mtime = os.path.getmtime(file_name)
	file_path = "/" + file_name
	
	with open(file_name, 'r') as f:
		data = f.read()
		start_time = time.time()
		try:
			dbx.files_upload(data, 
				file_path, 
				dropbox.files.WriteMode.overwrite, 
				True,
				client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
				mute=True)
			end_time = time.time()
			print("Uploading %.2f MB in %.3fs" % 
				(len(data) * 1.0 / MB, end_time - start_time))
		except dropbox.exceptions.ApiError as err:
			print 'Error uploading file'
			print err

def main():
	"""Main function
	Uploads a local folder content and then downloads it 
	"""
	
	if(len(sys.argv) < 2):
		print 'Usage: main.py local_directory_name'
		sys.exit(2)

	global LOCAL_PATH
	LOCAL_PATH = sys.argv[1]

	global UPLOAD_PATH
	UPLOAD_PATH = "/" + LOCAL_PATH

	dbx = configure_dropbox()

	print 'Generating random binary files...'
	generate_files()
	print 'Finished'

	print 'Upload files to Dropbox...'
	dir = os.path.dirname(__file__)
	for f in os.listdir("." + UPLOAD_PATH):
		file_name = os.path.join(dir, LOCAL_PATH + "/" + basename(f))
		upload_file(dbx, file_name)
	print 'Finished'

	print 'Download files from Dropbox...'
	for f in os.listdir("." + UPLOAD_PATH):
		download_file(dbx, basename(f))
	print 'Finished'


if __name__ == '__main__':
    main()
