import json
import string
import random
from json import JSONDecodeError
from datetime import datetime,date

def AutoGenerate_EventID():
    #generate a random Event ID
    Event_ID=''.join(random.choices(string.ascii_uppercase+string.digits,k=3))
    return Event_ID

def Register(type,member_json_file,organizer_json_file,Full_Name,Email,Password):
    '''Register the member/ogranizer based on the type with the given details'''
    if type.lower()=='organizer':
        f=open(organizer_json_file,'r+')
        d={
            "Full Name":Full_Name,
            "Email":Email,
            "Password":Password
        }
        try:
            content=json.load(f)
            if d not in content:
                content.append(d)
                f.seek(0)
                f.truncate()
                json.dump(content,f)
        except JSONDecodeError:
            l=[]
            l.append(d)
            json.dump(l,f)
        f.close()
    else:
        f=open(member_json_file,'r+')
        d={
            "Full Name":Full_Name,
            "Email":Email,
            "Password":Password
        }
        try:
            content=json.load(f)
            if d not in content:
                content.append(d)
                f.seek(0)
                f.truncate()
                json.dump(content,f)
        except JSONDecodeError:
            l=[]
            l.append(d)
            json.dump(l,f)
        f.close()


def Login(type,members_json_file,organizers_json_file,Email,Password):
    '''Login Functionality || Return True if successful else False'''
    d=0
    if type.lower()=='organizer':
        f=open(organizers_json_file,'r+')
    else:
        f=open(members_json_file,'r+')
    try:
        content=json.load(f)
    except JSONDecodeError:
        f.close()
        return False
    for i in range(len(content)):
        if content[i]["Email"]==Email and content[i]["Password"]==Password:
            d=1
            break
    if d==0:
        f.close()
        return False
    f.close()
    return True

def Create_Event(org,events_json_file,Event_ID,Event_Name,Start_Date,Start_Time,End_Date,End_Time,Users_Registered,Capacity,Availability):
    '''Create an Event with the details entered by organizer'''
    df={} 
    df["ID"]= Event_ID
    df["Name"]= Event_Name
    df["Organizer"]= org
    df["Start Date"]= Start_Date
    df["Start Time"]= Start_Time
    df["End Date"]= End_Date
    df["End Time"]= End_Time
    df["Users Registered"]= Users_Registered
    df["Capacity"]= Capacity
    df["Seats Available"]= Availability
    with open(events_json_file,"r") as f:
        try:
            data= json.load(f)
            data.append(df)
        except JSONDecodeError:
            data=[]
            data.append(df)
    with open(events_json_file,"w") as f:
        json.dump(data,f)
        
def View_Events(org,events_json_file):
    '''Return a list of all events created by the logged in organizer'''
    l=[]
    with open(events_json_file,"r") as f:
        try:
            js=json.load(f)
        except JSONDecodeError:
            return l
    for j in range(len(js)):
        if js[j]["Organizer"]==org:
            l.append(js[j])
        else:
            continue
    return l

def View_Event_ByID(events_json_file,Event_ID):
    '''Return details of the event for the event ID entered by user'''
    l=[]
    with open(events_json_file,"r") as f:
        try:
            js=json.load(f)
        except JSONDecodeError:
            return l
    for i in range(len(js)):
        if js[i]["ID"]==Event_ID:
            l.append(js[i])
        else:
            continue
    return l

def Update_Event(org,events_json_file,event_id,detail_to_be_updated,updated_detail):
    '''Update Event by ID || Take the key name to be updated from member, then update the value entered by user for that key for the selected event
    || Return True if successful else False'''
    with open(events_json_file,"r") as f:
        try:
            js=json.load(f)
        except JSONDecodeError:
            return False
        for i in range(len(js)):
            if js[i]["Organizer"]==org:
                js[i][detail_to_be_updated]= updated_detail
            else:
                continue
    with open(events_json_file,"w") as f:
        json.dump(js,f)
    return True

            
def Delete_Event(org,events_json_file,event_ID):
    '''Delete the Event with the entered Event ID || Return True if successful else False'''
    with open(events_json_file,"r") as f:
        try:
            js=json.load(f)
        except JSONDecodeError:
            return False
    for i in range(len(js)):
        if js[i]["ID"]==event_ID and js[i]["Organizer"]== org:
            js.remove(js[i])
        else:
            continue
    with open(events_json_file,"w") as f:
        json.dump(js,f)
    return True
        
def Register_for_Event(events_json_file,event_id,Full_Name):
    '''Register the logged in member in the event with the event ID entered by member. 
    (append Full Name inside the "Users Registered" list of the selected event)) 
    Return True if successful else return False'''
    date_today=str(date.today())
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    '''Write your code below this line'''
    with open(events_json_file,"r") as f:
        try:
            js=json.load(f)
        except JSONDecodeError:
            return False
    for k in range(len(js)):
        if js[k]["ID"] == event_id:
            if datetime.strptime(js[k]["Start Date"],"%Y-%m-%d") > datetime.strptime(date_today,"%Y-%m-%d"):
                js[k]["Users Registered"].append(Full_Name)
    with open(events_json_file,"w") as f:
        try:
            json.dump(js,f)
        except JSONDecodeError:
            return False
    return True

def fetch_all_events(events_json_file,Full_Name,event_details,upcoming_ongoing):
    '''View Registered Events | Fetch a list of all events of the logged in memeber'''
    '''Append the details of all upcoming and ongoing events list based on the today's date/time and event's date/time'''
    date_today=str(date.today())
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    '''Write your code below this line'''
    with open(events_json_file,'r') as f:
        try:
            js=json.load(f)
        except JSONDecodeError:
            return upcoming_ongoing
    for i in range(len(js)):
        if Full_Name in js[i]['Users Registered']:
            if datetime.strptime(js[i]["Start Date"],"%Y-%m-%d") == datetime.strptime(date_today,"%Y-%m-%d") and js[i]["Start Time"] >= current_time:
                upcoming_ongoing.append(js[i])
            elif datetime.strptime(js[i]["Start Date"],"%Y-%m-%d") > datetime.strptime(date_today,"%Y-%m-%d"):
                upcoming_ongoing.append(js[i])
            else:
                event_details.append(js[i])
        else:
            event_details.append(js[i])
    return upcoming_ongoing
                    
def Update_Password(members_json_file,Full_Name,new_password):
    '''Update the password of the member by taking a new passowrd || Return True if successful else return False'''
    with open(members_json_file,"r") as f:
        try:
            jm=json.load(f)
        except JSONDecodeError:
            return False
        for i in range(len(jm)):
            if jm[i]["Full Name"]== Full_Name:
                jm[i]["Password"]=new_password
    with open(members_json_file,"w") as f:
            json.dump(jm,f)
    return True

def View_all_events(events_json_file):
    '''Read all the events created | DO NOT change this function'''
    '''Already Implemented Helper Function'''
    details=[]
    f=open(events_json_file,'r')
    try:
        content=json.load(f)
        f.close()
    except JSONDecodeError:
        f.close()
        return details
    for i in range(len(content)):
        details.append(content[i])
    return details
