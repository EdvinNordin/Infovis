import pandas as pd
from bokeh.layouts import layout
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure, show
from bokeh.models.widgets import Panel, Tabs

dataset = pd.read_csv("pokedex_(Update_05.20).csv")
datasetCDS = ColumnDataSource(data=dataset)
total = dataset["hp"] + dataset["attack"] + dataset["sp_attack"] + dataset["defense"] + dataset["sp_defense"] + dataset[
    "speed"]

#adding total as a new column in datasetCDS
datasetCDS.data["total"]=total

zsrc = ColumnDataSource(data={'image':[z]})
"""hp = dataset["hp"]
attack = dataset["attack"]
defense = dataset["defense"]
sp_attack = dataset["sp_attack"]
sp_defense = dataset["sp_defense"]
speed = dataset["speed"]
total = dataset["hp"] + dataset["attack"] + dataset["sp_attack"] + dataset["defense"] + dataset["sp_defense"] + dataset[
    "speed"]
dex = dataset["pokedex_number"]"""


TOOLTIPS = [
    ("Pokedex", "@pokedex_number"),
    ("hp", "@hp"),
    ("attack", "@attack"),
    ("sp_attack", "@sp_attack"),
    ("defense", "@defense"),
    ("sp_defense", "@sp_defense"),
    ("speed", "@speed"),
]


php = figure(x_axis_label="total", y_axis_label="hp", tooltips=TOOLTIPS)
php.circle(x="total", y="hp", source=datasetCDS, color="black", size=3)
tab1 = Panel(child=php, title="hp")

patt = figure(x_axis_label="total", y_axis_label="attack", tooltips=TOOLTIPS)
patt.circle(x="total", y="attack", source=datasetCDS, color="black", size=3)
tab2 = Panel(child=patt, title="attack")

pspa = figure(x_axis_label="total", y_axis_label="sp_attack", tooltips=TOOLTIPS)
pspa.circle(x="total", y="sp_attack", source=datasetCDS, color="black", size=3)
tab3 = Panel(child=pspa, title="sp_attack")

pdef = figure(x_axis_label="total", y_axis_label="defense", tooltips=TOOLTIPS)
pdef.circle(x="total", y="defense", source=datasetCDS, color="black", size=3)
tab4 = Panel(child=pdef, title="defense")

pspd = figure(x_axis_label="total", y_axis_label="sp_defense", tooltips=TOOLTIPS)
pspd.circle(x="total", y="sp_defense", source=datasetCDS, color="black", size=3)
tab5 = Panel(child=pspd, title="sp_defense")

pspe = figure(x_axis_label="total", y_axis_label="speed", tooltips=TOOLTIPS)
pspe.circle(x="total", y="speed", source=datasetCDS, color="black", size=3)
tab6 = Panel(child=pspe, title="speed")

tabs = Tabs(tabs=[tab1, tab2, tab3, tab4, tab5, tab6])
# show result
show(tabs)

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