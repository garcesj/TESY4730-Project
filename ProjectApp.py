from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

# DBHOST = os.environ.get("DBHOST")
# DBPORT = os.environ.get("DBPORT")
# DBPORT = int(DBPORT)
# DBUSER = os.environ.get("DBUSER")
# DBPWD = os.environ.get("DBPWD")
# DATABASE = os.environ.get("DATABASE")

bucket= custombucket
region= customregion
table= customtable

db_conn = connections.Connection(
    host= customhost,
    port=3306,
    user= customuser,
    password= custompass,
    db= customdb
    
)
output = {}
table = 'destination';

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route("/addDestination", methods=['POST'])
def AddDestination():
    first_name = request.form['firstname']
    last_name = request.form['lastname']
    city = request.form['cityy']
    country = location = request.form['countryy']
    tripdate = request.form['datee']
    tripdescription = location = request.form['descriptionn']
    destination_image_file = request.files['destination_image_file']
  
    insert_sql = "INSERT INTO destination VALUES (%s, %s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    if destination_image_file.filename == "":
        return "Please select a file"

    try:
        
        cursor.execute(insert_sql,(first_name, last_name, city, country, tripdate, tripdescription))
        db_conn.commit()
        author_name = "" + first_name + " " + last_name
        # Uplaod image file in S3 #
        author_image_file_name_in_s3 = "trip"+str(author_name) + "_image_file"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=author_image_file_name_in_s3, Body=destination_image_file)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                author_image_file_name_in_s3)

            # Save image file metadata in DynamoDB #
            #print("Uploading to S3 success... saving metadata in dynamodb...")
        
            
            #try:
            #    dynamodb_client = boto3.client('dynamodb', region_name= customregion )
            #    dynamodb_client.put_item(
            #     TableName= customtable,
            #        Item={
            #         'empid': {
            #              'N': emp_id
            #          },
            #          'image_url': {
            #                'S': object_url
            #            }
            #        }
            #    )

            #except Exception as e:
            #    program_msg = "Flask could not update DynamoDB table with S3 object URL"
            #    return str(e)
        
        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('AddEmpOutput.html', name=emp_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)
