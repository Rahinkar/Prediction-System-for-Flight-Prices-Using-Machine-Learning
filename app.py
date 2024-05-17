from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd
import webbrowser
from geopy.geocoders import Nominatim
import json
import requests

geolocator = Nominatim(user_agent="travel")
travel_loc = ''

app = Flask(__name__)
model = pickle.load(open("model.sav", "rb"))


@app.route("/", methods = ["GET", "POST"])
def predict():
	global travel_loc
	if request.method == "POST":
		if request.form['sub'] == 'Submit':

			# Date_of_Journey
			date_dep = request.form["Dep_Time"]
			Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
			Journey_month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)
			# print("Journey Date : ",Journey_day, Journey_month)

			# Departure
			Dep_hour = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour)
			Dep_min = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute)
			# print("Departure : ",Dep_hour, Dep_min)

			# Arrival
			date_arr = request.form["Arrival_Time"]
			Arrival_hour = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").hour)
			Arrival_min = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").minute)
			# print("Arrival : ", Arrival_hour, Arrival_min)

			# Duration
			dur_hour = abs(Arrival_hour - Dep_hour)
			dur_min = abs(Arrival_min - Dep_min)
			# print("Duration : ", dur_hour, dur_min)

			# Total Stops
			Total_stops = int(request.form["stops"])
			# print(Total_stops)

			# Airline
			# AIR ASIA = 0 (not in column)
			airline=request.form['airline']
			if(airline=='Jet Airways'):
				Jet_Airways = 1
				IndiGo = 0
				Air_India = 0
				Multiple_carriers = 0
				SpiceJet = 0
				Vistara = 0
				GoAir = 0
				Multiple_carriers_Premium_economy = 0
				Jet_Airways_Business = 0
				Vistara_Premium_economy = 0
				Trujet = 0 

			elif (airline=='IndiGo'):
				Jet_Airways = 0
				IndiGo = 1
				Air_India = 0
				Multiple_carriers = 0
				SpiceJet = 0
				Vistara = 0
				GoAir = 0
				Multiple_carriers_Premium_economy = 0
				Jet_Airways_Business = 0
				Vistara_Premium_economy = 0
				Trujet = 0 

			elif (airline=='Air India'):
				Jet_Airways = 0
				IndiGo = 0
				Air_India = 1
				Multiple_carriers = 0
				SpiceJet = 0
				Vistara = 0
				GoAir = 0
				Multiple_carriers_Premium_economy = 0
				Jet_Airways_Business = 0
				Vistara_Premium_economy = 0
				Trujet = 0 
				
			elif (airline=='Multiple carriers'):
				Jet_Airways = 0
				IndiGo = 0
				Air_India = 0
				Multiple_carriers = 1
				SpiceJet = 0
				Vistara = 0
				GoAir = 0
				Multiple_carriers_Premium_economy = 0
				Jet_Airways_Business = 0
				Vistara_Premium_economy = 0
				Trujet = 0 
				
			elif (airline=='SpiceJet'):
				Jet_Airways = 0
				IndiGo = 0
				Air_India = 0
				Multiple_carriers = 0
				SpiceJet = 1
				Vistara = 0
				GoAir = 0
				Multiple_carriers_Premium_economy = 0
				Jet_Airways_Business = 0
				Vistara_Premium_economy = 0
				Trujet = 0 
				
			elif (airline=='Vistara'):
				Jet_Airways = 0
				IndiGo = 0
				Air_India = 0
				Multiple_carriers = 0
				SpiceJet = 0
				Vistara = 1
				GoAir = 0
				Multiple_carriers_Premium_economy = 0
				Jet_Airways_Business = 0
				Vistara_Premium_economy = 0
				Trujet = 0

			elif (airline=='GoAir'):
				Jet_Airways = 0
				IndiGo = 0
				Air_India = 0
				Multiple_carriers = 0
				SpiceJet = 0
				Vistara = 0
				GoAir = 1
				Multiple_carriers_Premium_economy = 0
				Jet_Airways_Business = 0
				Vistara_Premium_economy = 0
				Trujet = 0

			elif (airline=='Multiple carriers Premium economy'):
				Jet_Airways = 0
				IndiGo = 0
				Air_India = 0
				Multiple_carriers = 0
				SpiceJet = 0
				Vistara = 0
				GoAir = 0
				Multiple_carriers_Premium_economy = 1
				Jet_Airways_Business = 0
				Vistara_Premium_economy = 0
				Trujet = 0

			elif (airline=='Jet Airways Business'):
				Jet_Airways = 0
				IndiGo = 0
				Air_India = 0
				Multiple_carriers = 0
				SpiceJet = 0
				Vistara = 0
				GoAir = 0
				Multiple_carriers_Premium_economy = 0
				Jet_Airways_Business = 1
				Vistara_Premium_economy = 0
				Trujet = 0

			elif (airline=='Vistara Premium economy'):
				Jet_Airways = 0
				IndiGo = 0
				Air_India = 0
				Multiple_carriers = 0
				SpiceJet = 0
				Vistara = 0
				GoAir = 0
				Multiple_carriers_Premium_economy = 0
				Jet_Airways_Business = 0
				Vistara_Premium_economy = 1
				Trujet = 0
				
			elif (airline=='Trujet'):
				Jet_Airways = 0
				IndiGo = 0
				Air_India = 0
				Multiple_carriers = 0
				SpiceJet = 0
				Vistara = 0
				GoAir = 0
				Multiple_carriers_Premium_economy = 0
				Jet_Airways_Business = 0
				Vistara_Premium_economy = 0
				Trujet = 1

			else:
				Jet_Airways = 0
				IndiGo = 0
				Air_India = 0
				Multiple_carriers = 0
				SpiceJet = 0
				Vistara = 0
				GoAir = 0
				Multiple_carriers_Premium_economy = 0
				Jet_Airways_Business = 0
				Vistara_Premium_economy = 0
				Trujet = 0

			# print(Jet_Airways,
			#     IndiGo,
			#     Air_India,
			#     Multiple_carriers,
			#     SpiceJet,
			#     Vistara,
			#     GoAir,
			#     Multiple_carriers_Premium_economy,
			#     Jet_Airways_Business,
			#     Vistara_Premium_economy,
			#     Trujet)

			# Source
			# Banglore = 0 (not in column)
			Source = request.form["Source"]
			if (Source == 'Delhi'):
				s_Delhi = 1
				s_Kolkata = 0
				s_Mumbai = 0
				s_Chennai = 0

			elif (Source == 'Kolkata'):
				s_Delhi = 0
				s_Kolkata = 1
				s_Mumbai = 0
				s_Chennai = 0

			elif (Source == 'Mumbai'):
				s_Delhi = 0
				s_Kolkata = 0
				s_Mumbai = 1
				s_Chennai = 0

			elif (Source == 'Chennai'):
				s_Delhi = 0
				s_Kolkata = 0
				s_Mumbai = 0
				s_Chennai = 1

			else:
				s_Delhi = 0
				s_Kolkata = 0
				s_Mumbai = 0
				s_Chennai = 0

			# print(s_Delhi,
			#     s_Kolkata,
			#     s_Mumbai,
			#     s_Chennai)

			# Destination
			# Banglore = 0 (not in column)
			Source = request.form["Destination"]
			travel_loc = Source
			if (Source == 'Cochin'):
				d_Cochin = 1
				d_Delhi = 0
				d_New_Delhi = 0
				d_Hyderabad = 0
				d_Kolkata = 0
			
			elif (Source == 'Delhi'):
				d_Cochin = 0
				d_Delhi = 1
				d_New_Delhi = 0
				d_Hyderabad = 0
				d_Kolkata = 0

			elif (Source == 'New_Delhi'):
				d_Cochin = 0
				d_Delhi = 0
				d_New_Delhi = 1
				d_Hyderabad = 0
				d_Kolkata = 0

			elif (Source == 'Hyderabad'):
				d_Cochin = 0
				d_Delhi = 0
				d_New_Delhi = 0
				d_Hyderabad = 1
				d_Kolkata = 0

			elif (Source == 'Kolkata'):
				d_Cochin = 0
				d_Delhi = 0
				d_New_Delhi = 0
				d_Hyderabad = 0
				d_Kolkata = 1

			else:
				d_Cochin = 0
				d_Delhi = 0
				d_New_Delhi = 0
				d_Hyderabad = 0
				d_Kolkata = 0

			# print(
			#     d_Cochin,
			#     d_Delhi,
			#     d_New_Delhi,
			#     d_Hyderabad,
			#     d_Kolkata
			# )
			

		#     ['Total_Stops', 'Journey_day', 'Journey_month', 'Dep_hour',
		#    'Dep_min', 'Arrival_hour', 'Arrival_min', 'Duration_hours',
		#    'Duration_mins', 'Airline_Air India', 'Airline_GoAir', 'Airline_IndiGo',
		#    'Airline_Jet Airways', 'Airline_Jet Airways Business',
		#    'Airline_Multiple carriers',
		#    'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet',
		#    'Airline_Trujet', 'Airline_Vistara', 'Airline_Vistara Premium economy',
		#    'Source_Chennai', 'Source_Delhi', 'Source_Kolkata', 'Source_Mumbai',
		#    'Destination_Cochin', 'Destination_Delhi', 'Destination_Hyderabad',
		#    'Destination_Kolkata', 'Destination_New Delhi']
			
			prediction=model.predict([[
				Total_stops,
				Journey_day,
				Journey_month,
				Dep_hour,
				Dep_min,
				Arrival_hour,
				Arrival_min,
				dur_hour,
				dur_min,
				Air_India,
				GoAir,
				IndiGo,
				Jet_Airways,
				Jet_Airways_Business,
				Multiple_carriers,
				Multiple_carriers_Premium_economy,
				SpiceJet,
				Trujet,
				Vistara,
				Vistara_Premium_economy,
				s_Chennai,
				s_Delhi,
				s_Kolkata,
				s_Mumbai,
				d_Cochin,
				d_Delhi,
				d_Hyderabad,
				d_Kolkata,
				d_New_Delhi
			]])


			output=round(prediction[0],2)

			#-----------------Weather Forecast--------------------------------------------
			location = geolocator.geocode(travel_loc)
			weather_req_url = "https://api.darksky.net/forecast/b32c78b7b64e097aca1089f2590817d6/"+str(location.latitude)+","+str(location.longitude)
			r = requests.get(weather_req_url)
			weather_obj = json.loads(r.text)
			currently = weather_obj['currently']['summary']
			forecast = weather_obj["hourly"]["summary"]

			return render_template('home.html',prediction_text="Your Flight price is Rs. {}".format(output),current=currently,forecastwea=forecast)

		elif request.form['sub']=='Suggest Picnic Spots':
			webbrowser.open_new_tab('https://google.com/search?q='+'picnic spots near '+travel_loc)

		elif request.form['sub']=='Suggest Hotels':
			webbrowser.open_new_tab('https://google.com/search?q='+'hotels in '+travel_loc)		   


	return render_template("home.html")

@app.route("/hotel",methods=['GET','POST'])
def hotelprice():
	model = pickle.load(open("hotel.sav", "rb"))
	if request.method == 'POST':
		bedroom = int(request.form['bedroom'])
		bed = int(request.form['bed'])
		hotel = int(request.form['hotel'])
		pool = int(request.form['pool'])
		balcony = int(request.form['balcony'])
		distance = int(request.form['distance'])
		testSample = [[bedroom,bed,hotel,pool,balcony,distance]]
		price = model.predict(testSample)
		return render_template('hotel.html',price=price[0])
	return render_template('hotel.html')


if __name__ == "__main__":
	app.run(debug=True)
