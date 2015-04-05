import requests

def nearbyEvents(zipCode):
	#returns a dictionary in Json 
	endpoint = 'http://api.jambase.com/events'
	query_params={
		'api_key' : 've5rd2b62f7bj6uexj8evnrv',
		'zip' : zipCode,
		'page' : 0
		}
	response = requests.get(endpoint, params=query_params)
	data = response.json()	

	return reorganize(data["Events"])

def reorganize(dic):
	e1, e2 =[],[]

	for i in range(4):
		temp ={}
		temp["Location"] = dic[i]["Venue"]["Name"] + dic[i]["Venue"]["Address"] +", "+dic[i]["Venue"]["City"]
		temp["Artists"] = makeArtist(dic[i]["Artists"])
		temp["Date"], temp["Time"] = dateAndTime(dic[i]["Date"])
		temp["ticket"] =dic[i]["TicketUrl"]
		e1.append(temp)

	for i in range(5,9):
		temp ={}
		temp["Location"] = dic[i]["Venue"]["Name"] + dic[i]["Venue"]["Address"] +", "+dic[i]["Venue"]["City"]
		temp["Artists"] = makeArtist(dic[i]["Artists"])
		temp["Date"], temp["Time"] = dateAndTime(dic[i]["Date"])
		temp["ticket"] =dic[i]["TicketUrl"]
		e2.append(temp)

	return e1,e2

def makeArtist(lst):
	if len(lst) == 1:
		return lst[0]["Name"]
	elif len(lst) == 2:
		return lst[0]["Name"] + " and "+lst[1]["Name"]
	else:
		a = ''
		ran =  len(lst)-1
		if ran > 5:
			ran = 5
		for i in range(len(lst)-1):
			a+= lst[i]["Name"] +', '
		return a + "and " +  lst[-1]["Name"]

def dateAndTime(s):
	year,month,day = s.split("-")
	day, time = day.split("T")
	date = month + "/" + day + "/" + year

	if 12- int(time[:2]) > 0:
		time = time[:6]+'AM'
	elif int(time[:2]) == 0:
		time = '12'+time[2:6]+'PM'
	else:
		time = str(int(time[:2])-12)+time[2:6]+'PM'
	return date,time
