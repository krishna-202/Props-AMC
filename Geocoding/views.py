from django.shortcuts import render
import pandas as pd
import openpyxl
from django.http import HttpResponse
from googlemaps import Client as GoogleMaps

gmaps = GoogleMaps('API_KEY')
# Getting Geocode APIby passing API KEY


def home(request):
    if request.method == 'POST':
        excel_file=request.FILES['excel_file']    # Fetch xl file from user input
        data=pd.read_excel(excel_file)            # convert it to dataframe for further calculation
        data['long'] = ""                         # Define a longitude column in dataframe and it is set to Null
        data['lat'] = ""                          # Define a latitude column in dataframe and it is set to Null
        for i in range(len(data)):                # Iterate through each row of dataframe
            geocode_result = gmaps.geocode(data['address'][i]) # Get the geocode object for a address column
            data['lat'][i] = geocode_result[0]['geometry']['location'] ['lat'] # Fetch latitude and setit for lat column in dataframe
            data['long'][i] = geocode_result[0]['geometry']['location']['lng'] # Fetch longitude and set it for long column in dataframe

        data.to_excel(excel_file)  # Export dataframe to excel sheet which has new columns now
        response=HttpResponse(excel_file,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sh') # Define http response with content type as excel sheet
        response['Content-Disposition'] = 'attachment; filename=address_lat_long.xlsx'

    return render(request,'Geocoding/home.html') #If request is GET render home template
