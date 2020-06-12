import sys
import googlemaps
import pandas as pd
import xlsxwriter

df = pd.read_csv("POI.csv")
gmaps = googlemaps.Client(key='AIzaSyBoTm5PkWEBB94fUTauDclTB9DxDdV1ugw')
long = []
lat = []
address = []
ParkingId = []

totalNumbUrl = len(df)
time_remaining = totalNumbUrl
time_remaining = (time_remaining - 1)

# Geocoding an address
for i in range(0, len(df), 1):
    geocode_result = gmaps.geocode(df.iat[i, 0])
    time_remaining = time_remaining - 1
    sys.stdout.write('\r' + 'Current Url: ' + str(i) + ' Percentage: ' + str(
        round((i / totalNumbUrl) * 100)) + '%' + ' time remaining: ' + str(round(time_remaining / 60)) + " minutes ")
    try:
        lat.append(geocode_result[0]["geometry"]["location"]["lat"])
        long.append(geocode_result[0]["geometry"]["location"]["lng"])
        address.append(geocode_result[0]["formatted_address"])
    except:
        lat.append('none')
        long.append('none')
        address.append('none')

Data = {'longitude': long, 'lattitude': lat, 'address': address}

# Create a Pandas dataframe from the data.
df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in Data.items()]))

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('POILocations.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()
