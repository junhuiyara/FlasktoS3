import os
from flask import Flask, render_template, request, redirect, send_file
from boto3 import client
import boto3

session = boto3.Session(profile_name='personal')
s3 = session.client('s3')
BUCKET = "junhuis3test"
UPLOAD_FOLDER = ""
app = Flask(__name__)

#all the commands needed
def upload_file(file_name, bucket):
    """
    Function to upload a file to an S3 bucket
    """
    object_name = file_name
    response = s3.upload_file(file_name, bucket, object_name)

    return response

def download_file(file_name, bucket):
    """
    Function to download a given file from an S3 bucket
    """
    s3r = session.resource('s3')
    output = f"{file_name}"
    s3r.Bucket(bucket).download_file(file_name, output)

    return output

def list_files(bucket):
    """
    Function to list files in a given S3 bucket
    """
    contents = []
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        contents.append(item)

    return contents
##until here

@app.route("/")
def storage():
    contents = list_files("junhuis3test")
    return render_template('storage.html', contents=contents)


@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        upload_file(f"{f.filename}", BUCKET)

        return redirect("/")

@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKET)

        return send_file(output, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)