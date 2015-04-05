import request

def nearbyEvents(zipCode):
	#returns a dictionary in Json 
	endpoint = 'http://api.jambase.com/search'
	query_params={
		'apikey' : 've5rd2b62f7bj6uexj8evnrv',
		'zip' : zipCode
		}
	response = requests.get(endpoint, params=query_params)
	data = response.json	
	return data["Events"]