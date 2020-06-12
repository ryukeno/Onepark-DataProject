import sys
import pandas as pd
import xlrd
import googlemaps
from googlemaps.convert import format_float
import xlsxwriter
# Open excel files
pkFile=xlrd.open_workbook('parkingloctest.xlsx')
poiFile=xlrd.open_workbook('poiloctest.xlsx')

# Get the sheet from excel files
pkSheet=pkFile.sheet_by_name('Sheet1')
poiSheet=poiFile.sheet_by_name('Sheet1')

parkingName=[]
poisNames=[]
distanceTransitText=[]
distanceTransitValue=[]
durationTransit=[]
durationTransitV=[]
durationWalking=[]
durationWalkingV=[]
durationDriving=[]
durationDrivingV=[]
distanceWalkingText=[]
distanceWalkingValue=[]
distanceDrivingText = []
distanceDrivingValue = []

totalNumbRows = pkSheet.nrows-1
time_remaining=totalNumbRows

gmaps = googlemaps.Client(key='AIzaSyAM9X5_b1CnKJPdKyBOK-EHDaAe6gvlKgY')


# Loop through each row in parkingSheet
for i in range(pkSheet.nrows):
    if pkSheet.cell_value(i, 0) != 'longitude' and pkSheet.cell_value(i, 1) != 'latitude':
        time_remaining = time_remaining - 1
        sys.stdout.write(
            '\r'+'Current Url: '+str(i)+' Percentage: '+str(round((i/totalNumbRows)*100))+'%'+' time remaining: '+str(
                round(time_remaining/60))+" minutes ")
        for e in range(poiSheet.nrows ):
            if poiSheet.cell_value(e 1,) != 'longitude' and poiSheet.cell_value(e, 2) != 'latitude':
                print(poiSheet.cell_value(e, 1))
                originLong=format_float(pkSheet.cell_value(i,0))
                originLat=format_float(pkSheet.cell_value(i,1))
                destiLong=format_float(poiSheet.cell_value(e,1))
                destLat=format_float(poiSheet.cell_value(e,2))
                origin=(originLat,originLong)
                destination=(destLat,destiLong)
                #transitresult=gmaps.distance_matrix(origin,destination,mode='transit')
                try:
                    transitresult = gmaps.distance_matrix(origin, destination, mode='transit')
                    if len(transitresult)!=0 and len(transitresult['rows'][0]["elements"][0]["distance"]["text"]) != 0:
                        parkingName.append(pkSheet.cell_value(i, 3))
                        poisNames.append(poiSheet.cell_value(e, 4))
                        distanceTransitText.append(transitresult['rows'][0]["elements"][0]["distance"]["text"])
                        distanceTransitValue.append(transitresult['rows'][0]["elements"][0]["distance"]["value"])
                        durationTransit.append(transitresult['rows'][0]["elements"][0]["duration"]["text"])
                        durationTransitV.append(transitresult['rows'][0]["elements"][0]["duration"]["value"])

                    walkingresult= gmaps.distance_matrix(origin,destination,mode='walking')
                    if len(walkingresult) != 0 and len(walkingresult['rows'][0]["elements"][0]["distance"]["text"]) != 0:
                        distanceWalkingText.append(walkingresult['rows'][0]["elements"][0]["distance"]["text"])
                        distanceWalkingValue.append(walkingresult['rows'][0]["elements"][0]["distance"]["value"])
                        durationWalking.append(walkingresult['rows'][0]["elements"][0]["duration"]["text"])
                        durationWalkingV.append(walkingresult['rows'][0]["elements"][0]["duration"]["value"])

                    drivingresult= gmaps.distance_matrix(origin,destination,mode='driving')
                    if len(drivingresult) != 0 and len(drivingresult['rows'][0]["elements"][0]["distance"]["text"]) != 0:
                        distanceDrivingText.append(drivingresult['rows'][0]["elements"][0]["distance"]["text"])
                        distanceDrivingValue.append(drivingresult['rows'][0]["elements"][0]["distance"]["value"])
                        durationDriving.append(drivingresult['rows'][0]["elements"][0]["duration"]["text"])
                        durationDrivingV.append(drivingresult['rows'][0]["elements"][0]["duration"]["value"])

                except:
                    parkingName.append(pkSheet.cell_value(i, 3))
                    poisNames.append(poiSheet.cell_value(e, 4))
                    distanceTransitText.append('none')
                    distanceTransitValue.append('none')
                    distanceWalkingText.append('none')
                    distanceWalkingValue.append('none')
                    distanceDrivingText.append('none')
                    distanceDrivingValue.append('none')
                    durationTransit.append('none')
                    durationTransitV.append('none')
                    durationWalking.append('none')
                    durationWalkingV.append('none')
                    durationDriving.append('none')
                    durationDrivingV.append('none')


Data={'Parking Names':parkingName,
    'POI Name':poisNames,
    'Distance Walking':distanceWalkingText,
    'Distance Walking value':distanceWalkingValue,
    'Distance Transit':distanceTransitText,
    'Distance Transit value':distanceTransitValue,
    'Distance Driving':distanceDrivingText,
    'Distance Driving value':distanceDrivingValue,
    'Duration by walking':durationWalking,
    'Duration by walking Value':durationWalkingV,
    'Duration by public transport':durationTransit,
    'Duration by public transport Value':durationTransitV,
    'Duration by car':durationDriving,
    'Duration by car value':durationDrivingV}

# Create a Pandas dataframe from the data.

df=pd.DataFrame(dict([(k, pd.Series(v)) for k,v in Data.items()]))

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer=pd.ExcelWriter('try.xlsx',engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer,sheet_name='Sheet 1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()