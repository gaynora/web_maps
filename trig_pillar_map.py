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
               #attr='OS',
               control_scale=True,
               )


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
            <img src="{row["Image"]}" alt="Still to visit" style="width:200px;">'
    popup = folium.Popup(popup_content, max_width=300)
    folium.Marker([row['lat'], row['long']], popup=popup,
                  icon=folium.DivIcon(html=f"""
                                      <div style="font-size: 10px; color: black;">               
                                      <i class="glyphicon glyphicon-hdd"></i>
                                      </div>
                                      """
                      )
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

# add button to locate individual via their device on a map
folium.plugins.LocateControl().add_to(m)

m.save(outfile='trig_pillar_map.html')

# ADD LEGEND, TITLE
# COLOUR MARKERS ON VISITED OR NOT
# SHOW SEPERATE CONNIE LAYER
# ADD PROW, OPEN ACCESS AREAS VECTOR TILES TIPPECANOE or QGIS QTILE RASTER TILES