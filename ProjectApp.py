from flask import Flask, render_template, request
#from pymysql import connections
import pymysql
import os
import boto3
#from config import *
import config
app = Flask(__name__)

# DBHOST = os.environ.get("DBHOST")
# DBPORT = os.environ.get("DBPORT")
# DBPORT = int(DBPORT)
# DBUSER = os.environ.get("DBUSER")
# DBPWD = os.environ.get("DBPWD")
# DATABASE = os.environ.get("DATABASE")

#bucket= custombucket
#region= customregion
#table= customtable

db_conn = pymysql.connect(
    host= 'destinations.coajuzoc6wxq.us-west-2.rds.amazonaws.com',
    port= 3306,
    user= 'dbuser',
    password= 'dbpassword',
    db= 'destination')

output = {}
table = 'destination';

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/adddest", methods=['POST'])
def addDestination():
    first_name = request.form["firstname"]
    last_name = request.form["lastname"]
    city = request.form["cityy"]
    country = request.form["countryy"]
    date = request.form["datee"]
    descript = request.form["descriptionn"]
    #emp_image_file = request.files['emp_image_file']
    
    author_name = "" + first_name + " " + last_name
    
    cursor = db_conn.cursor()
    
    #1st attempt that kinda WORKED - meh
    #insert_sql = "INSERT INTO destination VALUES ('hello','my','name','is','big','daddy')"
    #cursor.execute(insert_sql)
    #db_conn.commit()
    #
    #
    #+++++++++++FULLY WORKED 100% +++++++++++++++++
    cursor.execute("INSERT INTO destination VALUES (%s,%s,%s,%s,%s,%s)",(first_name,last_name,city,country,date,descript))
    db_conn.commit()
    
    return render_template('dataposted.html', name=author_name)

@app.route("/getdest", methods=['GET','POST'])
def getDestination():
    headings = ("By", "Location", "Trip Details")

    try:
        output = {}
        cursor = db_conn.cursor()
    
        select_sql = "SELECT * from destination"
        #cursor.execute(select_sql)
        
        #result = cursor.fetchone(cursor.execute(select_sql))
        result = cursor.fetchall()
        
        for row in result:
            by = row[0]# + " " + row[1]
            location = row[2]# + ", " + row[3]
            details = row[5]
            data = (by,location,details) 
        #    print("By: ", row[0])
        #    print(" ", row[1])
        #    print("Location: ", row[2])
        #    print(", ", row[3])
        #    print("Date of Trip: ", row[3])
        #    print("Details: ", row[5])
        #    print('\n')
            
        #cursor.close()
        
        #for row in result:
        #output["first_name"] = result[0]
        #output["last_name"] = result[1]
        #output["city"] = result[2]
        #output["country"] = result[3]
        #output["date"] = result[4]
        #output["descript"] = result[5]
        
        #author_name = "" + output["first_name"] + " " + output["last_name"]
        #loca = "" + output["city"] + ", " + output["country"]

    except Exception as e:
        return render_template('error.html')

    #return render_template('viewdata.html', by=author_name,location=loca, description=output["descript"])
    
    return render_template('viewdata.html',headings=headings, data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)