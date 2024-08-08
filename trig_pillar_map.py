# -*- coding: utf-8 -*-
"""
Boilerplate for a Folium map as a wrapper to Leaflet.js 
with bootstrap icons / pop-ups with images / 
csv derived locations from dataframe coords / user geolocate / OS and OSM tile options
Trip pillars were the context

@author: gaynora
"""

import pandas
import folium
from folium.plugins import LocateControl
from folium.plugins import MeasureControl

# read trig pillar data
df = pandas.read_csv('trig_pillars_current_accessible_4326.csv')


# Define  OS MAPS API Web Map Tile Service
wmts_path = 'https://api.os.uk/maps/raster/v1/wmts?key=cf29UaahD1kovSGU2x3wyFwW09bizUGK'

# OS Maps API (WMTS) endpoint path
wmts_endpoint = 'https://api.os.uk/maps/raster/v1/wmts?'

# Define WMTS parameters 
key = 'cf29UaahD1kovSGU2x3wyFwW09bizUGK'
service = 'wmts'
request = 'GetTile'
version = '2.0.0'
style = 'default'
# 'Outdoor' style base map in Pseudo Mercator projection for web mapping
layer = 'Outdoor_3857'
tileMatrixSet = 'EPSG:3857'
tileMatrix = 'EPSG:3857:{z}'
tileRow = '{y}'
tileCol ='{x}'

# Represent WMTS parameters in a dictionary
params_wmts = {'key':key, 
              'service':service, 
              'request':request,
              'version':version,
              'style':style,
              'layer':layer,
              'tileMatrixSet':tileMatrixSet,
              'tileMatrix':tileMatrix,
              'tileRow':tileRow,
              'tileCol':tileCol}

# Construct WMTS API path
wmts_path = wmts_endpoint + \
           ('key={key}&'
            'service={service}&'
            'request={request}&'
            'version={version}&'
            'style={style}&'
            'layer={layer}&'
            'tileMatrixSet={tileMatrixSet}&'
            'tileMatrix={tileMatrix}&'
            'tileRow={tileRow}&'
            'tileCol={tileCol}').format(**params_wmts)

print('=> Constructed OS Maps API URL: {}'.format(wmts_path))

#Create map object:
m = folium.Map(location=[53.780948, -1.959399],
               zoom_start=7,
               min_zoom=7, 
               max_zoom=16,
               tiles=None,
               attr='Method uses open data', 
               control_scale=True,
               )

# add brief text to act as title / basic legend
map_title = "Accessible trig pillars"
title_html = f'<h4 style="position:absolute;z-index:100000;left:1vw; bottom: 8vh; color:#000000; background-color:#ffffff" >{map_title}</h4>'
m.get_root().html.add_child(folium.Element(title_html))
map_title = "Visited in blue"
title_html = f'<h4 style="position:absolute;z-index:100000;left:1vw; bottom:5vh; color:#0000FF; background-color:#ffffff" >{map_title}</h4>'
m.get_root().html.add_child(folium.Element(title_html))
map_title = 'Method uses open data from OSGB, Natural England, NatureScot, NRW, Scottish Gov, Local Authorities and the brilliant www.rowmaps.com'
title_html = f'<h6 style="position:absolute;z-index:100000;left:1vw; bottom:1vh; color:#000000; background-color:#ffffff" >{map_title}</h6>'
m.get_root().html.add_child(folium.Element(title_html))

# Function to determine marker color based on category
def get_marker_color(category):
    color_dict = {
        'Yes': 'blue',
        'No': 'black'
    }
    return color_dict.get(category, 'black')

# Add markers with popups containing images and custom icon
for index, row in df.iterrows():
    popup_content = f'<h4>{row["Trig Name"]}</h4>\
        <h5>Height: {row["HEIGHT"]} metres</h5>\
        <h5>CROW access land: {row["CROW"]}</h5>\
        <h5>Country Park: {row["CountryPar"]}</h5>\
        <h5>Public park / garden / playspace / playing field, Scottish golf course: {row["OSOpenGS"]}</h5>\
        <h5>Public Right of Way within 10 metres: {row["PROW10M"]}</h5>\
        <h5>Public road within 10 metres: {row["ROAD10M"]}</h5>\
        <h5>Crops (Scotland): {row["Scotcrop"]}</h5>\
            <img src="{row["Image"]}" alt="No image" style="width:200px;">'
    popup = folium.Popup(popup_content, max_width=300)
    color_ = get_marker_color(row['Visited'])
    folium.Marker([row['lat'], row['long']], popup=popup,
                  icon=folium.DivIcon(html=f"""
                                      <div style="font-size: 10px; color: {color_};">               
                                      <i class="glyphicon glyphicon-hdd"></i>
                                      </div>
                                      """)
                      
                  #icon=folium.DivIcon(html=f"""<a>
                         # <div style="font-size: 10em;">
                          #<div style="width: 10px;
                                      #height: 10px;
                                      #border: 1px solid black;
                                      #border-radius: 5px;
                                      #background-color: black;">
                          #</div>
                      #</div>
                      #</a>""")
                      ).add_to(m)

# add OS and OSM tile layers
folium.TileLayer(tiles=wmts_path, name='Ordnance Survey', attr='Contains OS Crown Copyright',
                 control=True, show=True).add_to(m)
folium.TileLayer("OpenStreetMap", name='Open Street Map', show=False, control=True).add_to(m)

# Add context layers
# Tiles here

# add layer control - this needs to be placed last in the code after all layers are declared
folium.LayerControl().add_to(m) 
'''
The method utilises the Geolocation API and getCurrentPosition() which queries the positioning hardware to get information.
By default, getCurrentPosition() tries to answer as fast as possible with a low accuracy result. 
Devices with a GPS, for example, can take a minute or more to get a GPS fix, so less accurate data (IP location or Wi-Fi) may be returned 
to getCurrentPosition(). 
In rural areas where Google's 'Improve Location Accuracy' setting is used, it counterintuitively reduces the accuracy of the estimated location 
coordinates: the tool is better used without this setting enabled.
'''

# add button to locate individual via their device on a map
folium.plugins.LocateControl().add_to(m)

# add measure distance tool to map
m.add_child(MeasureControl(#position="top left",
                           active_color="red",
                           completed_color="red",
                           primary_length_unit='kilometers', 
                           secondary_length_unit='miles', 
                           primary_area_unit='sqmeters', 
                           secondary_area_unit='acres')
            )

m.save(outfile='trig_pillar_map.html')

