import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

def volcano_color(el):
    if el < 1000:
        return 'blue'
    elif el < 2000:
        return 'orange'
    else:
        return 'red'

map = folium.Map(location=[40,-100], zoom_start=6, tiles="Stamen Terrain")
fgv = folium.FeatureGroup(name="Volcanoes")

for lt, ln, el, nm in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (nm, nm, el), width=200, height=100)
    #fg.add_child(folium.Marker(location=[lt,ln], popup=str(el), icon=folium.Icon(color='red')))
    #fg.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon = folium.Icon(color = volcano_color(el))))
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=5, popup=folium.Popup(iframe),
    fill_color = volcano_color(el), fill_opacity=0.8, color='gray'))

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
style_function = lambda x: {'fillColor' : 'green' if x['properties']['POP2005'] < 10000000
else 'orange' if x['properties']['POP2005'] < 20000000 else 'red'}))  #to form polygons

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("Map1.html")
