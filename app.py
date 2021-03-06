# -*- coding: utf-8 -*-

import os

# import Libraries 


import numpy as np
import json
import pandas as pd
import plotly.express as px


import config 


#Setup Mapbox Token

px.set_mapbox_access_token(config.mapbox_token)

# Read geojson file 
# Datasource Credits to Camâra Municipal de Lisboa 

with open('Limites_Cartografia.geojson', 'r') as fp:
    jdata = json.load( fp)

 
# create a new feature called ID for every record in the geojson file     

for k in range(len(jdata['features'])):
    jdata['features'][k]['id'] = k


# Import CSV file
# Data Source:
# Year: 2021 - INE 
# Year 2018 - 2020 Dummy Data 

df= pd.read_csv("ine_lx_2016_2021_quarters.csv")

# Assign variable to columns for melt 
dates = df.columns[3:]

# Transform DF to long format 
df1 = pd.melt(df, id_vars = ['ID','NOME'],
                      value_vars=dates,     
                      var_name='DATA',
                      value_name='PRICE'
                      )


# Mapdesign - Where the magic happens 

# Explanation

# We use dataframe "df" as reference. The "jdata" dataframe as our geojson reference
# Locations are equal our dataframe "ID" that correspond to the "id" in the geojson
# "id" is the featurekey by default. If your common column name is different change accordingly


fig = px.choropleth_mapbox(df1, geojson=jdata, locations='ID', color='PRICE',              # color is based on the df dataframe "PRICE"
                           color_continuous_scale="Viridis_r",                            # Choose a continuous color scale. "_r" reverses the color scale. 
                           range_color=(650, 6000),                                       # Set a scale range so that is fixed and doesn't change at every step of the animation
                           animation_frame='DATA',                                        # Set an animation frame based on our dataframe column "ANO" (means "YEAR" in Portuguese) 
                           mapbox_style="carto-positron",                                 # Set mapbox map style 
                           zoom=12.07, center = {"lat": 38.743646, "lon": -9.160204},     # You can get these values by going to Mapbox Chart Studio, setting your view, and then click on "Settings"
                           opacity=1,                                                     # The opacity you want to use. This depends on what your final objective is. 
                           labels={'PRICE':'Preço por m2','NOME':'Freguesia'},            # Set Hover Labels

                          )


fig.update_layout(margin={"r":50,"t":100,"l":50,"b":50}, showlegend=True,                                # Set Margins and Mapbox style. You can create your on Mapbox Chart Studio. 
                  mapbox_style="mapbox://styles/vostpt/ckofpf18i1fdb17phhv9tkqkm"
                  )

fig.update_mapboxes(bearing=-34.40, pitch=60.50)                                        # You can get these values by going to Mapbox Chart Studio, setting your view, and then click on "Settings"

fig.update_layout(title_text="Preço Médio M2 em Lisboa",
                  title_font_size=30)



# DashAPP 

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    dcc.Graph(figure=fig,style={'height':'100vh'})
    ],
)

if __name__ == '__main__':
  app.run_server(debug=True) 
