from flask import Blueprint, render_template ,request,redirect,send_file
from flask_login import login_required, current_user
import os
import boto3
from boto3 import client

session = boto3.Session(profile_name='personal')
s3 = session.client('s3')
s3r = session.resource('s3')
BUCKETNAME = "junhuis3test"
UPLOAD_FOLDER = ""


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)



def upload_file(file_name, bucket):
    """
    Function to upload a file to an S3 bucket
    """
    object_name = file_name
    response = s3.upload_file(file_name, bucket, object_name)

    return response

def list_files(bucket):
    """
    Function to list files in a given S3 bucket
    """
    contents = []
    print("Contents" in s3.list_objects(Bucket=BUCKETNAME))

    if "Contents" in s3.list_objects(Bucket=BUCKETNAME):
        for item in s3.list_objects(Bucket=BUCKETNAME)['Contents']:
            contents.append(item)


    return contents

def download_file(file_name, bucket):
    """
    Function to download a given file from an S3 bucket
    """
    output = file_name
    output = output  
    print(output)
    s3r.Bucket(bucket).download_file(file_name, output)

    return output
##until here


@login_required
@main.route("/storage")
def storage():
    contents = list_files(BUCKETNAME)
    return render_template('storage.html', contents=contents)

@main.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        #upload the absolute path of the filename
        print(f)
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))	 
        upload_file(f.filename, BUCKETNAME)	

        return redirect("/storage")

@main.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKETNAME)

        return send_file(output, as_attachment=True)

@main.route("/delete/<filename>", methods=['GET'])
def delete(filename):
    if request.method == 'GET':
        s3r.Object(BUCKETNAME, filename).delete()

        return redirect("/storage")