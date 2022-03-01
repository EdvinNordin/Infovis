import pandas as pd

from bokeh.embed import json_item
from bokeh.layouts import layout, gridplot
from bokeh.models import HoverTool, ColumnDataSource, CustomJSHover, CategoricalColorMapper
from bokeh.plotting import figure, show
from bokeh.models.widgets import Panel, Tabs, Select

dataframe = pd.read_csv("pokedex_(Update_05.20).csv")
datasetCDS = ColumnDataSource(data=dataframe)
total = dataframe["hp"] + dataframe["attack"] + dataframe["sp_attack"] + dataframe["defense"] + dataframe["sp_defense"] + dataframe[
    "speed"]

#adding total as a new column in datasetCDS
datasetCDS.data["total"] = total

dataframe['formPN'] = dataframe['pokedex_number'].apply(lambda x: '{0:0>3}'.format(x))
#creates the url to the images

lastPDnum = 0
Fval = 2
for x in range(len(datasetCDS.data["index"])):

    if lastPDnum == datasetCDS.data['pokedex_number'][x]:
        dataframe['url'] = 'https://assets.pokemon.com/assets/cms2/img/pokedex/detail/' + dataframe['formPN'].astype(str) + '_f2.png'
        dataframe['url'] = dataframe['url'].str.replace(' ', '-')
        dataframe['url'] = dataframe['url'].str.lower()

        Fval = Fval + 1
    else:
        dataframe['url'] = 'https://assets.pokemon.com/assets/cms2/img/pokedex/detail/' + dataframe['formPN'].astype(str) + '.png'
        dataframe['url'] = dataframe['url'].str.replace(' ', '-')
        dataframe['url'] = dataframe['url'].str.lower()

        lastPDnum = datasetCDS.data['pokedex_number'][x]
        Fval = 2



datasetCDS.data["url"] = dataframe['url']
#dataframe.to_excel("test1.xlsx")
sizeCoeff = 2

datasetCDS.data['hpSize'] = dataframe['hp']/sizeCoeff
datasetCDS.data['attackSize'] = dataframe['attack']/sizeCoeff
datasetCDS.data['sp_attackSize'] = dataframe['sp_attack']/sizeCoeff
datasetCDS.data['defenseSize'] = dataframe['defense']/sizeCoeff
datasetCDS.data['sp_defenseSize'] = dataframe['sp_defense']/sizeCoeff
datasetCDS.data['speedSize'] = dataframe['speed']/sizeCoeff

TOOLTIPS = """
    <div style="width: 150px;>
    
        <div style="display: grid;">
            <span style="font-size: 17px; font-weight: bold;">@name</span></div>
        <div style="display: grid;"><span style="font-size: 14px; font-weight: bold;">Pokédex: @pokedex_number</span></div>
        </div style="display: grid;">
        <div style="position: bottom;">
        
        <div style="display: grid; margin-bottom: 2%;">
            <img src="@url" height="100%" alt="@name" width="100%"
                style=" float:right; margin: 0px;"
                border="1">
            </img>
        </div>
        <div style="position: relative; text-align: center; font-size: 10px; vertical-align: bottom; ">
        
        
          <div style="display: inline-block;vertical-align: bottom;">@hp         <div style="width:30px;height:@hpSize;        border:1px solid #000;background-color: lightblue;"></div>HP</div>
          <div style="display: inline-block;vertical-align: bottom;">@attack     <div style="width:30px;height:@attackSize;    border:1px solid #000;background-color: lightblue;"></div>Atk</div>
          <div style="display: inline-block;vertical-align: bottom;">@sp_attack  <div style="width:30px;height:@sp_attackSize; border:1px solid #000;background-color: lightblue;"></div>Sp.Atk</div>
          <div style="display: inline-block;vertical-align: bottom;">@defense    <div style="width:30px;height:@defenseSize;   border:1px solid #000;background-color: lightblue;"></div>Def</div>
          <div style="display: inline-block;vertical-align: bottom;">@sp_defense <div style="width:30px;height:@sp_defenseSize;border:1px solid #000;background-color: lightblue;"></div>Sp.Def</div>
          <div style="display: inline-block;vertical-align: bottom;">@speed      <div style="width:30px;height:@speedSize;     border:1px solid #000;background-color: lightblue;"></div>Spe</div>

        </div>
        
   
        
    </div>
"""

color_mapper = CategoricalColorMapper(palette=["#EAA3DC", "#B8B8D0", "#765747", "#7636F6", "#745797", "#BF9F38", "#A5B82B",
                                               "#FF4980", "#AC8FEF", "#E9C26E", "#AF399D", "#D51C0D", "#7FDADA", "#55CA59",
                                               "#FFCE2E", "#5591F0", "#FF7919", "#A9A879"],
                                      factors=["Fairy", "Steel", "Dark", "Dragon", "Ghost", "Rock", "Bug", "Psychic",
                                               "Flying", "Ground", "Poison", "Fight", "Ice", "Grass", "Electric",
                                               "Water", "Fire", "Normal"])


php = figure(x_axis_label="Total", y_axis_label="HP", tooltips=TOOLTIPS, active_scroll="wheel_zoom")
php.circle(x="total", y="hp", source=datasetCDS, name="mycircle", color={'field': 'type_1', 'transform': color_mapper}, size=5)
tab1 = Panel(child=php, title="HP")

patt = figure(x_axis_label="Total", y_axis_label="Attack", tooltips=TOOLTIPS, active_scroll="wheel_zoom")
patt.circle(x="total", y="attack", source=datasetCDS, color={'field': 'type_1', 'transform': color_mapper}, size=5)
tab2 = Panel(child=patt, title="Attack")

pspa = figure(x_axis_label="Total", y_axis_label="Special Attack", tooltips=TOOLTIPS, active_scroll="wheel_zoom")
pspa.circle(x="total", y="sp_attack", source=datasetCDS, color={'field': 'type_1', 'transform': color_mapper}, size=5)
tab3 = Panel(child=pspa, title="Special Attack")

pdef = figure(x_axis_label="Total", y_axis_label="Defense", tooltips=TOOLTIPS, active_scroll="wheel_zoom")
pdef.circle(x="total", y="defense", source=datasetCDS, color={'field': 'type_1', 'transform': color_mapper}, size=5)
tab4 = Panel(child=pdef, title="Defense")

pspd = figure(x_axis_label="Total", y_axis_label="Special Defense", tooltips=TOOLTIPS, active_scroll="wheel_zoom")
pspd.circle(x="total", y="sp_defense", source=datasetCDS, color={'field': 'type_1', 'transform': color_mapper}, size=5)
tab5 = Panel(child=pspd, title="Special Defense")

pspe = figure(x_axis_label="Total", y_axis_label="Speed", tooltips=TOOLTIPS, active_scroll="wheel_zoom")
pspe.circle(x="total", y="speed", source=datasetCDS, color={'field': 'type_1', 'transform': color_mapper}, size=5)
tab6 = Panel(child=pspe, title="Speed")

tabs = Tabs(tabs=[tab1, tab2, tab3, tab4, tab5, tab6])



p=gridplot([[tabs]], toolbar_location=None)

# show result
show(p)




"""
''' An interactivate categorized chart based on a movie dataset.
This example shows the ability of Bokeh to create a dashboard with different
sorting options based on a given dataset.

'''
import sqlite3 as sql
from os.path import dirname, join

import numpy as np
import pandas.io.sql as psql

from bokeh.io import curdoc, show
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput
from bokeh.plotting import figure
from bokeh.sampledata.movies_data import movie_path

conn = sql.connect(movie_path)
query = open(join(dirname(__file__), 'query.sql')).read()
movies = psql.read_sql(query, conn)

movies["color"] = np.where(movies["Oscars"] > 0, "orange", "grey")
movies["alpha"] = np.where(movies["Oscars"] > 0, 0.9, 0.25)
movies.fillna(0, inplace=True)  # just replace missing values with zero
movies["revenue"] = movies.BoxOffice.apply(lambda x: '{:,d}'.format(int(x)))

with open(join(dirname(__file__), "razzies-clean.csv")) as f:
    razzies = f.read().splitlines()
movies.loc[movies.imdbID.isin(razzies), "color"] = "purple"
movies.loc[movies.imdbID.isin(razzies), "alpha"] = 0.9

axis_map = {
    "Tomato Meter": "Meter",
    "Numeric Rating": "numericRating",
    "Number of Reviews": "Reviews",
    "Box Office (dollars)": "BoxOffice",
    "Length (minutes)": "Runtime",
    "Year": "Year",
}

desc = Div(text=open(join(dirname(__file__), "description.html")).read(), sizing_mode="stretch_width")

# Create Input controls
reviews = Slider(title="Minimum number of reviews", value=80, start=10, end=300, step=10)
min_year = Slider(title="Year released", start=1940, end=2014, value=1970, step=1)
max_year = Slider(title="End Year released", start=1940, end=2014, value=2014, step=1)
oscars = Slider(title="Minimum number of Oscar wins", start=0, end=4, value=0, step=1)
boxoffice = Slider(title="Dollars at Box Office (millions)", start=0, end=800, value=0, step=1)
genre = Select(title="Genre", value="All",
               options=open(join(dirname(__file__), 'genres.txt')).read().split())
director = TextInput(title="Director name contains")
cast = TextInput(title="Cast names contains")
x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="Tomato Meter")
y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()), value="Number of Reviews")

# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(x=[], y=[], color=[], title=[], year=[], revenue=[], alpha=[]))

TOOLTIPS=[
    ("Title", "@title"),
    ("Year", "@year"),
    ("$", "@revenue")
]

p = figure(height=600, width=700, title="", toolbar_location=None, tooltips=TOOLTIPS, sizing_mode="scale_both")
p.circle(x="x", y="y", source=source, size=7, color="color", line_color=None, fill_alpha="alpha")


def select_movies():
    genre_val = genre.value
    director_val = director.value.strip()
    cast_val = cast.value.strip()
    selected = movies[
        (movies.Reviews >= reviews.value) &
        (movies.BoxOffice >= (boxoffice.value * 1e6)) &
        (movies.Year >= min_year.value) &
        (movies.Year <= max_year.value) &
        (movies.Oscars >= oscars.value)
    ]
    if (genre_val != "All"):
        selected = selected[selected.Genre.str.contains(genre_val)==True]
    if (director_val != ""):
        selected = selected[selected.Director.str.contains(director_val)==True]
    if (cast_val != ""):
        selected = selected[selected.Cast.str.contains(cast_val)==True]
    return selected


def update():
    df = select_movies()
    x_name = axis_map[x_axis.value]
    y_name = axis_map[y_axis.value]

    p.xaxis.axis_label = x_axis.value
    p.yaxis.axis_label = y_axis.value
    p.title.text = "%d movies selected" % len(df)
    source.data = dict(
        x=df[x_name],
        y=df[y_name],
        color=df["color"],
        title=df["Title"],
        year=df["Year"],
        revenue=df["revenue"],
        alpha=df["alpha"],
    )

controls = [reviews, boxoffice, genre, min_year, max_year, oscars, director, cast, x_axis, y_axis]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

inputs = column(*controls, width=320)

l = column(desc, row(inputs, p), sizing_mode="scale_both")

update()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "Movies"

show(p)"""
