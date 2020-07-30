import os
from flask import Flask, render_template, request, redirect, send_file
from boto3 import client
import boto3

session = boto3.Session(profile_name='personal')
s3 = session.client('s3')
s3r = session.resource('s3')
BUCKETNAME = "junhuis3test"
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
    output = f"{file_name}"
    s3r.Bucket(bucket).download_file(file_name, output)

    return output

def list_files(bucket):
    """
    Function to list files in a given S3 bucket
    """
    contents = []
    print("Contents" in s3.list_objects(Bucket=BUCKETNAME))
    print("aaaaaaaaa")

    if "Contents" in s3.list_objects(Bucket=BUCKETNAME):
        for item in s3.list_objects(Bucket=BUCKETNAME)['Contents']:
            contents.append(item)


    return contents
##until here

@app.route("/")
def storage():
    contents = list_files(BUCKETNAME)
    return render_template('storage.html', contents=contents)


@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        print(f)
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))	 
        upload_file(f"{f.filename}", BUCKETNAME)	

        return redirect("/")

@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKETNAME)

        return send_file(output, as_attachment=True)

@app.route("/delete/<filename>", methods=['GET'])
def delete(filename):
    if request.method == 'GET':
        s3r.Object(BUCKETNAME, filename).delete()

        return redirect("/")

""""
todo
user authentication
access/download only if got authentication
connect via db(NOT S3)
filter and search in db

maybe get good at webscraping and also dockerise this whole thing...
"""
"""for request.arg and to conduct filtering
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)"""

if __name__ == '__main__':
    app.run(debug=True)