import mysql.connector
import requests
import json
import os
import datetime

mydb = mysql.connector.connect(host="localhost", user="root", passwd="YOUR MYSQL PASSWORD HERE", database="YOUR DATABASE NAME HERE") 

mycursor = mydb.cursor()
mycursor.execute("SET time_zone = '+00:00'")

url = "https://api-football-v1.p.rapidapi.com/v3/teams"
now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

team = input("ENTER NAME OF THE TEAM TO GET THE DETAILS: ")
query_string = {"name":team}
headers = {
    'x-rapidapi-key': "Your rapid api key here",
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }
response = requests.request("GET", url, headers=headers, params=query_string)
response_text = response.text
with open("file1.json", "w") as file1:
    file1.write(response_text)
file1.close()
with open("file1.json","r+") as file:
    data = json.load(file)
    name = data['parameters']['name']
    country = data['response'][0]['team']['country']
    found = data['response'][0]['team']['founded']
    venue = data['response'][0]['venue']['name']
    capacity = data['response'][0]['venue']['capacity']
    city = data['response'][0]['venue']['city']
    team_logo = data['response'][0]['team']['logo']
    venue_image = data['response'][0]['venue']['image']
    print("Name: {}\nCountry: {}\nFound: {}\nVenue: {}\nCity: {}\nCapacity: {}\nTeam Logo Image: {}\nVenue Image: {}".format(name, country, found, venue, city, capacity, team_logo, venue_image))
os.remove("file1.json")

# EXECUTE THIS COMMAND FIRST...
# mycursor.execute("CREATE TABLE footballData (name varchar(30), found int, country varchar(10), venue varchar(30), capacity int, searchtime DATETIME);")

query = "INSERT INTO footballData (name, found, country, venue, capacity, searchtime) VALUES (%s,%s,%s,%s,%s,%s)"
values = [(name, found, country, venue, capacity, now.strftime('%Y-%m-%d %H:%M:%S'))]

mycursor.executemany(query, values)
mydb.commit()

mycursor.close()
mydb.close()