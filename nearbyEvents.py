import requests

def nearbyEvents(zipCode):
	#returns a dictionary in Json 
	endpoint = 'http://api.jambase.com/events'
	query_params={
		'api_key' : 've5rd2b62f7bj6uexj8evnrv',
		'zip' : zipCode,
		'page' : 0,
		'radius':50
		}
	response = requests.get(endpoint, params=query_params)
	data = response.json()	

	return reorganize(data["Events"], zipCode)

def reorganize(dic, zipCode):
	e1, e2 =[],[]
	c1, c2 = 4,4
	i = 0
	while c1 != 0:
		if dic[i]["Venue"]["ZipCode"].isnumeric() and abs(int(dic[i]["Venue"]["ZipCode"]) -int(zipCode)) <5000:
			temp ={}
			temp["Location"] = dic[i]["Venue"]["Name"] + dic[i]["Venue"]["Address"] +", "+dic[i]["Venue"]["City"]
			temp["Artists"] = makeArtist(dic[i]["Artists"])
			temp["Date"], temp["Time"] = dateAndTime(dic[i]["Date"])
			temp["ticket"] =dic[i]["TicketUrl"]
			e1.append(temp)
			c1-=1
		i += 1

	while c2 != 0:
		if dic[i]["Venue"]["ZipCode"].isnumeric() and abs(int(dic[i]["Venue"]["ZipCode"]) -int(zipCode)) <5000:
			temp ={}
			temp["Location"] = dic[i]["Venue"]["Name"] + dic[i]["Venue"]["Address"] +", "+dic[i]["Venue"]["City"]
			temp["Artists"] = makeArtist(dic[i]["Artists"])
			temp["Date"], temp["Time"] = dateAndTime(dic[i]["Date"])
			temp["ticket"] =dic[i]["TicketUrl"]
			e2.append(temp)
			c2-=1
		i += 1

	return e1,e2

def makeArtist(lst):
	if len(lst) == 1:
		return lst[0]["Name"]
	elif len(lst) == 2:
		return lst[0]["Name"] + " and "+lst[1]["Name"]
	else:
		a = ''
		ran =  len(lst)-1
		if ran > 3:
			ran = 3
		for i in range(ran-1):
			a+= lst[i]["Name"] +', '
		return a + "and " +  lst[-1]["Name"]

def dateAndTime(s):
	year,month,day = s.split("-")
	day, time = day.split("T")
	date = month + "/" + day + "/" + year

	if 12- int(time[:2]) > 0:
		time = time[:5]+'AM'
	elif int(time[:2])-12 == 0:
		time = '12'+time[2:5]+'PM'
	else:
		time = str(int(time[:2])-12)+time[2:5]+'PM'
	return date,time
