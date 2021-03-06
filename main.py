# Imports libraries
#import urllib.request #(only need if you want to check url)

import pandas as pd #used to import the dataset

from bokeh.events import ButtonClick
from bokeh.io import curdoc
from bokeh.layouts import layout, gridplot, row, column
from bokeh.models import ColumnDataSource, CategoricalColorMapper, CheckboxButtonGroup, CDSView, BooleanFilter, Div, \
    BoxSelectTool, LassoSelectTool
from bokeh.models.widgets import Panel, Tabs, Button, RadioButtonGroup
from bokeh.plotting import figure, show
from bokeh.server.server import Server

# Load in database with pandas
dataframe = pd.read_csv("pokedex_(Update_05.20).csv")
# Load in the database with bokeh
datasetCDS = ColumnDataSource(data=dataframe)

# Adds all stats to a total for the axis
total = dataframe["hp"] + dataframe["attack"] + dataframe["sp_attack"] + dataframe["defense"] + dataframe[
    "sp_defense"] + dataframe["speed"]

# Adding total as a new column in datasetCDS
datasetCDS.data["total"] = total

# Stores Pokédex number as "001" instead of "1" in formPN
dataframe['formPN'] = dataframe['pokedex_number'].apply(lambda x: '{0:0>3}'.format(x))
datasetCDS.data["formPN"] = dataframe['formPN']
datasetCDS.data["gen"] = dataframe['name']
for x in range(len(datasetCDS.data["index"])):
    datasetCDS.data["gen"][x] = str(datasetCDS.data["generation"][x])


# Creates the url to the images

def image(url):
    request = urllib.request.Request(url)
    request.get_method = lambda: 'HEAD'

    try:
        urllib.request.urlopen(request)
        return True
    except urllib.request.HTTPError:
        return False


# uncomment "if image(url):" and tab line below it to run the url checker to make sure every pokemon has an image. It
# will take alot longer to load.
urlvar = [""] * len(datasetCDS.data["index"])
datasetCDS.data["url"] = urlvar
for x in range(len(datasetCDS.data["index"])):

    datasetCDS.data['url'][x] = 'https://assets.pokemon.com/assets/cms2/img/pokedex/detail/' + \
                                datasetCDS.data['formPN'][x] + '.png'

    if datasetCDS.data['pokedex_number'][x] == datasetCDS.data['pokedex_number'][x - 1]:
        url = 'https://assets.pokemon.com/assets/cms2/img/pokedex/detail/' + datasetCDS.data['formPN'][x] + '_f2.png'
        # if image(url):
        datasetCDS.data['url'][x] = url

    if datasetCDS.data['pokedex_number'][x] == datasetCDS.data['pokedex_number'][x - 2]:
        url = 'https://assets.pokemon.com/assets/cms2/img/pokedex/detail/' + datasetCDS.data['formPN'][x] + '_f3.png'
        # if image(url):
        datasetCDS.data['url'][x] = url

    if datasetCDS.data['pokedex_number'][x] == datasetCDS.data['pokedex_number'][x - 3]:
        # url = 'https://assets.pokemon.com/assets/cms2/img/pokedex/detail/' + datasetCDS.data['formPN'][x] + '_f4.png'
        # if image(url):
        datasetCDS.data['url'][x] = url

# Reads the data from each stat from the database and scales them to a coefficent
sizeCoeff = 2
datasetCDS.data['hpSize'] = dataframe['hp'] / sizeCoeff
datasetCDS.data['attackSize'] = dataframe['attack'] / sizeCoeff
datasetCDS.data['sp_attackSize'] = dataframe['sp_attack'] / sizeCoeff
datasetCDS.data['defenseSize'] = dataframe['defense'] / sizeCoeff
datasetCDS.data['sp_defenseSize'] = dataframe['sp_defense'] / sizeCoeff
datasetCDS.data['speedSize'] = dataframe['speed'] / sizeCoeff

# HTML and CSS to the hovering function
TOOLTIPS = """
    <div style="width: 150px;">
        <div style="display: grid;">
            <span style="font-size: 17px; font-weight: bold;">@name</span></div>
            <div style="display: grid;"><span style="font-size: 14px; font-weight: bold;">Pokédex: @pokedex_number</span></div>
        </div style="display: grid;">

        <div style="display: grid; margin-bottom: 2%;">
            <img src="@url" height="100%" alt="@name" width="100%"
                style=" float:right; margin: 0px;"
                border="1">
            </img>
        </div>
        <div id="" style="position: relative; text-align: center; font-size: 10px; vertical-align: bottom; ">
        
          <div style="display: inline-block;vertical-align: bottom;">@hp         <div 
          style="width:30px;height:@hpSize;        border:1px solid #000;background-color: lightblue;"></div>HP</div> 
          <div style="display: inline-block;vertical-align: bottom;">@attack     <div 
          style="width:30px;height:@attackSize;    border:1px solid #000;background-color: 
          lightblue;"></div>Atk</div> <div style="display: inline-block;vertical-align: bottom;">@sp_attack  <div 
          style="width:30px;height:@sp_attackSize; border:1px solid #000;background-color: 
          lightblue;"></div>Sp.Atk</div> <div style="display: inline-block;vertical-align: bottom;">@defense    <div 
          style="width:30px;height:@defenseSize;   border:1px solid #000;background-color: 
          lightblue;"></div>Def</div> <div style="display: inline-block;vertical-align: bottom;">@sp_defense <div 
          style="width:30px;height:@sp_defenseSize;border:1px solid #000;background-color: 
          lightblue;"></div>Sp.Def</div> <div style="display: inline-block;vertical-align: bottom;">@speed      <div 
          style="width:30px;height:@speedSize;     border:1px solid #000;background-color: lightblue;"></div>Spe</div> 

        </div>
    </div>
"""
# The existing types and their correlated color and maps them together
types = ["Fairy", "Steel", "Dark", "Dragon", "Ghost", "Rock", "Bug", "Psychic",
         "Flying", "Ground", "Poison", "Fighting", "Ice", "Grass", "Electric",
         "Water", "Fire", "Normal"]
colors = ["#EAA3DC", "#B8B8D0", "#765747", "#7636F6", "#745797", "#BF9F38", "#A5B82B",
          "#FF4980", "#AC8FEF", "#E9C26E", "#AF399D", "#D51C0D", "#7FDADA", "#55CA59",
          "#FFCE2E", "#5591F0", "#FF7919", "#A9A879"]
color_mapper = CategoricalColorMapper(
    palette=colors,
    factors=types)

#color column in the dataset return a hexcode
def color(type):
    for j in range(len(types)):
        if type == types[j]:
            return colors[j]

#interaction options with the plots
options = dict(tools="pan,wheel_zoom,lasso_select,box_select,reset")

#the first view when opening the page
view = CDSView(source=datasetCDS, filters=[])

# Code for the scatter plot, labels and tabs
php = figure(x_axis_label="Total", y_axis_label="HP", tooltips=TOOLTIPS, active_scroll="wheel_zoom", **options)
php.circle(x="total", y="hp", source=datasetCDS, alpha=0.3, hover_alpha=1,
           color={'field': 'type_1', 'transform': color_mapper}, size=5, name="circle", view=view)
tab1 = Panel(child=php, title="HP")

patt = figure(x_axis_label="Total", y_axis_label="Attack", tooltips=TOOLTIPS, active_scroll="wheel_zoom", **options)
patt.circle(x="total", y="attack", source=datasetCDS, alpha=0.3, hover_alpha=1,
            color={'field': 'type_1', 'transform': color_mapper}, size=5, name="circle", view=view)
tab2 = Panel(child=patt, title="Attack")

pspa = figure(x_axis_label="Total", y_axis_label="Special Attack", tooltips=TOOLTIPS, active_scroll="wheel_zoom",
              **options)
pspa.circle(x="total", y="sp_attack", source=datasetCDS, alpha=0.3, hover_alpha=1,
            color={'field': 'type_1', 'transform': color_mapper}, size=5, name="circle", view=view)
tab3 = Panel(child=pspa, title="Special Attack")

pdef = figure(x_axis_label="Total", y_axis_label="Defense", tooltips=TOOLTIPS, active_scroll="wheel_zoom", **options)
pdef.circle(x="total", y="defense", source=datasetCDS, alpha=0.3, hover_alpha=1,
            color={'field': 'type_1', 'transform': color_mapper}, size=5, name="circle", view=view)
tab4 = Panel(child=pdef, title="Defense")

pspd = figure(x_axis_label="Total", y_axis_label="Special Defense", tooltips=TOOLTIPS, active_scroll="wheel_zoom",
              **options)
pspd.circle(x="total", y="sp_defense", source=datasetCDS, alpha=0.3, hover_alpha=1,
            color={'field': 'type_1', 'transform': color_mapper}, size=5, name="circle", view=view)
tab5 = Panel(child=pspd, title="Special Defense")

pspe = figure(x_axis_label="Total", y_axis_label="Speed", tooltips=TOOLTIPS, active_scroll="wheel_zoom", **options)
pspe.circle(x="total", y="speed", source=datasetCDS, alpha=0.3, hover_alpha=1,
            color={'field': 'type_1', 'transform': color_mapper}, size=5, name="circle", view=view)
tab6 = Panel(child=pspe, title="Speed")

tabs = Tabs(tabs=[tab1, tab2, tab3, tab4, tab5, tab6])

# Code for the parallell coordinates figure
lineFig = figure(tooltips=TOOLTIPS, active_scroll="wheel_zoom", **options)

#parallell coordinates plot with color
mult = [[0] * 6] * len(datasetCDS.data["index"])
colorRange = [""] * len(datasetCDS.data["index"])

for i in range(len(datasetCDS.data["index"])):
    mult[i] = [datasetCDS.data["hp"][i],
               datasetCDS.data["attack"][i],
               datasetCDS.data["sp_attack"][i],
               datasetCDS.data["defense"][i],
               datasetCDS.data["sp_defense"][i],
               datasetCDS.data["speed"][i]]

    colorRange[i] = color(datasetCDS.data['type_1'][i])

#creating more dataframes in the dataset for the multiline
#only works with numbers for some reason :(
dataframe['names'] = [["1", "2", "3", "4", "5", "6"]] * len(datasetCDS.data["index"])
datasetCDS.data['names'] = dataframe['names']

dataframe['mult'] = mult
datasetCDS.data['mult'] = dataframe['mult']

datasetCDS.data['color'] = colorRange

#adding all the lines to the figure
lineFig.multi_line("names", "mult", source=datasetCDS, color="color", alpha=0.3, hover_alpha=1, view=view,
                   name="circle")

#show the plots in a gridpattern
gp = gridplot([[tabs, lineFig]], toolbar_location="below")

#array to see which gen is active
genList = [0] * 8

#functions to change the array on button press
def gen1(in_active):
    if in_active:
        genList[0] = 1
    else:
        genList[0] = 0


def gen2(in_active):
    if in_active:
        genList[1] = 2
    else:
        genList[1] = 0


def gen3(in_active):
    if in_active:
        genList[2] = 3
    else:
        genList[2] = 0


def gen4(in_active):
    if in_active:
        genList[3] = 4
    else:
        genList[3] = 0


def gen5(in_active):
    if in_active:
        genList[4] = 5
    else:
        genList[4] = 0


def gen6(in_active):
    if in_active:
        genList[5] = 6
    else:
        genList[5] = 0


def gen7(in_active):
    if in_active:
        genList[6] = 7
    else:
        genList[6] = 0


def gen8(in_active):
    if in_active:
        genList[7] = 8
    else:
        genList[7] = 0

#array for the types
typeList = [""] * 18


#functions to change the array on button press
def Fairy(in_active):
    if in_active:
        typeList[8] = "Fairy"
    else:
        typeList[8] = ""


def Steel(in_active):
    if in_active:
        typeList[1] = "Steel"
    else:
        typeList[1] = ""


def Dark(in_active):
    if in_active:
        typeList[2] = "Dark"
    else:
        typeList[2] = ""


def Dragon(in_active):
    if in_active:
        typeList[3] = "Dragon"
    else:
        typeList[3] = ""


def Ghost(in_active):
    if in_active:
        typeList[4] = "Ghost"
    else:
        typeList[4] = ""


def Rock(in_active):
    if in_active:
        typeList[5] = "Rock"
    else:
        typeList[5] = ""


def Bug(in_active):
    if in_active:
        typeList[6] = "Bug"
    else:
        typeList[6] = ""


def Psychic(in_active):
    if in_active:
        typeList[7] = "Psychic"
    else:
        typeList[7] = ""


def Flying(in_active):
    if in_active:
        typeList[8] = "Flying"
    else:
        typeList[8] = ""


def Ground(in_active):
    if in_active:
        typeList[9] = "Ground"
    else:
        typeList[9] = ""


def Poison(in_active):
    if in_active:
        typeList[10] = "Poison"
    else:
        typeList[10] = ""


def Fighting(in_active):
    if in_active:
        typeList[11] = "Fighting"
    else:
        typeList[11] = ""


def Ice(in_active):
    if in_active:
        typeList[12] = "Ice"
    else:
        typeList[12] = ""


def Grass(in_active):
    if in_active:
        typeList[13] = "Grass"
    else:
        typeList[13] = ""


def Electric(in_active):
    if in_active:
        typeList[14] = "Electric"
    else:
        typeList[14] = ""


def Water(in_active):
    if in_active:
        typeList[15] = "Water"
    else:
        typeList[15] = ""


def Fire(in_active):
    if in_active:
        typeList[16] = "Fire"
    else:
        typeList[16] = ""


def Normal(in_active):
    if in_active:
        typeList[17] = "Normal"
    else:
        typeList[17] = ""


statusList = [""] * 4


def isNormal(in_active):
    if in_active:
        statusList[0] = "Normal"
    else:
        statusList[0] = ""


def isSub(in_active):
    if in_active:
        statusList[1] = "Sub Legendary"
    else:
        statusList[1] = ""


def isLegend(in_active):
    if in_active:
        statusList[2] = "Legendary"
    else:
        statusList[2] = ""


def isMyth(in_active):
    if in_active:
        statusList[3] = "Mythical"
    else:
        statusList[3] = ""


gen_list = [gen1, gen2, gen3, gen4, gen5, gen6, gen7, gen8]
# https://stackoverflow.com/questions/46899348/bokeh-how-to-loop-through-checkboxbuttongroup?rq=1

booleans = [False] * len(datasetCDS.data["index"])

#on button click run this
def generation(attr, old, new):

    last_clicked_ID = list(set(old) ^ set(new))[0]  # [0] there will always be just one different element at a time
    last_clicked_button_stuff = gen_list[last_clicked_ID]
    in_active = last_clicked_ID in new
    last_clicked_button_stuff(in_active)

    #change the output depending on what is buttons are activated
    for i in range(len(datasetCDS.data["index"])):
        # 1
        if datasetCDS.data['generation'][i] in genList and (
                datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][i] in typeList) and \
                datasetCDS.data['status'][i] in statusList:
            booleans[i] = True
        # 2
        elif genList == [0] * 8 and (
                datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][i] in typeList) and \
                datasetCDS.data['status'][i] in statusList:
            booleans[i] = True
        # 3
        elif datasetCDS.data['generation'][i] in genList and typeList == [""] * 18 and datasetCDS.data['status'][
            i] in statusList:
            booleans[i] = True
        # 4
        elif datasetCDS.data['generation'][i] in genList and (
                datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][
            i] in typeList) and statusList == [""] * 4:
            booleans[i] = True
        # 5
        elif genList == [0] * 8 and typeList == [""] * 18 and datasetCDS.data['status'][i] in statusList:
            booleans[i] = True
        # 6
        elif genList == [0] * 8 and (datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][
            i] in typeList) and statusList == [""] * 4:
            booleans[i] = True
        # 7
        elif datasetCDS.data['generation'][i] in genList and typeList == [""] * 18 and statusList == [""] * 4:
            booleans[i] = True
        # 8
        else:
            booleans[i] = False

    #update the views of all plot based on the active buttons
    php.select(name='circle')[0].view = CDSView(source=datasetCDS, filters=[BooleanFilter(booleans)])
    patt.select(name='circle')[0].view = CDSView(source=datasetCDS, filters=[BooleanFilter(booleans)])
    pspa.select(name='circle')[0].view = CDSView(source=datasetCDS, filters=[BooleanFilter(booleans)])
    pdef.select(name='circle')[0].view = CDSView(source=datasetCDS, filters=[BooleanFilter(booleans)])
    pspd.select(name='circle')[0].view = CDSView(source=datasetCDS, filters=[BooleanFilter(booleans)])
    pspe.select(name='circle')[0].view = CDSView(source=datasetCDS, filters=[BooleanFilter(booleans)])
    lineFig.select(name='circle')[0].view = CDSView(source=datasetCDS, filters=[BooleanFilter(booleans)])

#the generation filter buttons
GENS = ["1", "2", "3", "4", "5", "6", "7", "8"]
gens = CheckboxButtonGroup(labels=GENS, active=[])
gens.on_change('active', generation)

#list of the type functions
type_list = [Fairy, Steel, Dark, Dragon, Ghost, Rock, Bug, Psychic, Flying, Ground, Poison, Fighting, Ice, Grass,
             Electric, Water, Fire, Normal]

# https://stackoverflow.com/questions/46899348/bokeh-how-to-loop-through-checkboxbuttongroup?rq=1

#on button click run this
def typing(attr, old, new):
    last_clicked_ID = list(set(old) ^ set(new))[0]  # [0] there will always be just one different element at a time
    last_clicked_button_stuff = type_list[last_clicked_ID]
    in_active = last_clicked_ID in new
    last_clicked_button_stuff(in_active)

    # change the output depending on what is buttons are activated
    for i in range(len(datasetCDS.data["index"])):
        # 1
        if datasetCDS.data['generation'][i] in genList and (
                datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][i] in typeList) and \
                datasetCDS.data['status'][i] in statusList:
            booleans[i] = True
        # 2
        elif genList == [0] * 8 and (
                datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][i] in typeList) and \
                datasetCDS.data['status'][i] in statusList:
            booleans[i] = True
        # 3
        elif datasetCDS.data['generation'][i] in genList and typeList == [""] * 18 and datasetCDS.data['status'][
            i] in statusList:
            booleans[i] = True
        # 4
        elif datasetCDS.data['generation'][i] in genList and (
                datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][
            i] in typeList) and statusList == [""] * 4:
            booleans[i] = True
        # 5
        elif genList == [0] * 8 and typeList == [""] * 18 and datasetCDS.data['status'][i] in statusList:
            booleans[i] = True
        # 6
        elif genList == [0] * 8 and (datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][
            i] in typeList) and statusList == [""] * 4:
            booleans[i] = True
        # 7
        elif datasetCDS.data['generation'][i] in genList and typeList == [""] * 18 and statusList == [""] * 4:
            booleans[i] = True
        # 8
        else:
            booleans[i] = False
    # update the views of all plot based on the active buttons
    php.select(name='circle')[0].view = CDSView(source=datasetCDS, filters=[BooleanFilter(booleans)])
    patt.select(name='circle')[0].view = CDSView(source=datasetCDS, filters=[BooleanFilter(booleans)])
    pspa.select(name='circle')[0].view = CDSView(source=datasetCDS, filters=[BooleanFilter(booleans)])
    pdef.select(name='circle')[0].view = CDSView(source=datasetCDS, filters=[BooleanFilter(booleans)])
    pspd.select(name='circle')[0].view = CDSView(source=datasetCDS, filters=[BooleanFilter(booleans)])
    pspe.select(name='circle')[0].view = CDSView(source=datasetCDS, filters=[BooleanFilter(booleans)])
    lineFig.select(name='circle')[0].view = CDSView(source=datasetCDS, filters=[BooleanFilter(booleans)])

#all type buttons
TYPES = ["Fairy", "Steel", "Dark", "Dragon", "Ghost", "Rock", "Bug", "Psychic",
         "Flying", "Ground", "Poison", "Fighting", "Ice", "Grass", "Electric",
         "Water", "Fire", "Normal"]
types = CheckboxButtonGroup(labels=TYPES, active=[])
types.on_change('active', typing)

#list of the status functions
status_list = [isNormal, isSub, isLegend, isMyth]

# https://stackoverflow.com/questions/46899348/bokeh-how-to-loop-through-checkboxbuttongroup?rq=1

#on button click run this
def whatSatus(attr, old, new):
    last_clicked_ID = list(set(old) ^ set(new))[0]  # [0] there will always be just one different element at a time
    last_clicked_button_stuff = status_list[last_clicked_ID]
    in_active = last_clicked_ID in new
    last_clicked_button_stuff(in_active)

    # change the output depending on what is buttons are activated
    for i in range(len(datasetCDS.data["index"])):
        # 1
        if datasetCDS.data['generation'][i] in genList and (
                datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][i] in typeList) and \
                datasetCDS.data['status'][i] in statusList:
            booleans[i] = True
        # 2
        elif genList == [0] * 8 and (
                datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][i] in typeList) and \
                datasetCDS.data['status'][i] in statusList:
            booleans[i] = True
        # 3
        elif datasetCDS.data['generation'][i] in genList and typeList == [""] * 18 and datasetCDS.data['status'][
            i] in statusList:
            booleans[i] = True
        # 4
        elif datasetCDS.data['generation'][i] in genList and (
                datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][
            i] in typeList) and statusList == [""] * 4:
            booleans[i] = True
        # 5
        elif genList == [0] * 8 and typeList == [""] * 18 and datasetCDS.data['status'][i] in statusList:
            booleans[i] = True
        # 6
        elif genList == [0] * 8 and (datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][
            i] in typeList) and statusList == [""] * 4:
            booleans[i] = True
        # 7
        elif datasetCDS.data['generation'][i] in genList and typeList == [""] * 18 and statusList == [""] * 4:
            booleans[i] = True
        # 8
        else:
            booleans[i] = False

    # update the views of all plot based on the active buttons
    php.select(name='circle')[0].view = CDSView(source=datasetCDS, filters=[BooleanFilter(booleans)])
    patt.select(name='circle')[0].view = CDSView(source=datasetCDS, filters=[BooleanFilter(booleans)])
    pspa.select(name='circle')[0].view = CDSView(source=datasetCDS, filters=[BooleanFilter(booleans)])
    pdef.select(name='circle')[0].view = CDSView(source=datasetCDS, filters=[BooleanFilter(booleans)])
    pspd.select(name='circle')[0].view = CDSView(source=datasetCDS, filters=[BooleanFilter(booleans)])
    pspe.select(name='circle')[0].view = CDSView(source=datasetCDS, filters=[BooleanFilter(booleans)])
    lineFig.select(name='circle')[0].view = CDSView(source=datasetCDS, filters=[BooleanFilter(booleans)])

#all status buttons
STATUS = ["Normal", "Sub Legendary", "Legendary", "Mythical"]
status = CheckboxButtonGroup(labels=STATUS, active=[])
status.on_change('active', whatSatus)

#titles to the filter options
typeDiv = Div(text="<b>Types</b>")
genDiv = Div(text="<b>Generation</b>")
statusDiv = Div(text="<b>Status</b>")

#placement on the page
lower = row(column(genDiv, gens), column(statusDiv, status))
options = column(typeDiv, types, lower)
layout = column(gp, options)

#show the page
# dataframe.to_excel("test.xlsx")
curdoc().add_root(layout)
show(layout)

# in terminal: bokeh serve --show main.py
#on file directory to be able to use the filtering functions
