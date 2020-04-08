import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import plotly.express as px
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input,Output


# external CSS stylesheets
external_stylesheets = [
   {
       'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
       'rel': 'stylesheet',
       'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
       'crossorigin': 'anonymous'
   }
]

# To Store Total Cases Dataset
Total=pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")

# To Store Decased Dataset
Deceased=pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")

# To Store Alive Dataset
Recovered = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")

# Grouping Total Number Of Cases On the Basis Of Country
TotalCases = Total.iloc[:,[1,-1]]
TotalCases = TotalCases.groupby(['Country/Region']).sum()

# Grouping Total Deaths On The Basis Of Country
TotalDeaths = Deceased.iloc[:,[1,-1]]
TotalDeaths = TotalDeaths.groupby(['Country/Region']).sum()

# Grouping Total Alive Cases Together
TotalRecovered = Recovered.iloc[:,[1,-1]]
TotalRecovered = TotalRecovered.groupby(['Country/Region']).sum()

# Creating New Dataset Of All Parameters
Data = TotalCases.merge(TotalDeaths, left_on='Country/Region', right_on='Country/Region')
Data = Data.merge(TotalRecovered, left_on='Country/Region', right_on='Country/Region')
Data = Data.reset_index()


# Adding Total Active Cases Column To Dataset
TotalActiveCases = Data.iloc[:,1]-Data.iloc[:,2]-Data.iloc[:,3]
Data["Active"] = TotalActiveCases
Data.rename(columns={Data.columns[1]:"Total Cases", Data.columns[2]: "Total Deaths", Data.columns[3]: "Total Recovery", Data.columns[4]: "Total Active"}, inplace=True)

# Calculating Total Figures Of Death, Recovery, Active and Total Cases
TotalCasesFigures = Data.iloc[:,1].sum()
DeathsFigures = Data.iloc[:,2].sum()
RecoveredFigures = Data.iloc[:,3].sum()
ActiveFigures = Data.iloc[:,4].sum()

# Extracting Dates
Dates = Total.columns
Dates = Dates[4:]

# Storing Total, Deaths, Recovered in X,Y,Z respectively
x = Total.groupby('Country/Region')
y = Deceased.groupby('Country/Region')
z = Recovered.groupby('Country/Region')


options=[
    {'label':'Total Cases', 'value':1},
    {'label':'Active', 'value':4},
    {'label':'Recovered', 'value':3},
    {'label':'Deaths','value':2}
]

#for selecting country for line plot
def unique(x):
     return list(dict.fromkeys(x))
country=Total["Country/Region"].tolist()
country=unique(country)

options2=[]
for i in country:
    options2.append({'label':i,'value':i})


app=dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <meta name="description" content="Graphical Analysis of covid-19(corona virus)">
        <meta name="keywords" content="Covid-19, covid19, corona, coronavirus, statistics, count">
        <title>Corona Virus Pandemic</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div([
    html.H1("Coronavirus live updates", style={ 'text-align':'center'}),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Cases", className='text-light'),
                    html.H4(TotalCasesFigures, className='text-light')
                ], className='card-body')
             ], className='card bg-danger'),
        ], className='col-md-3 padit'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Active Cases", className='text-light'),
                    html.H4(ActiveFigures, className='text-light')
                ], className='card-body')
             ], className='card bg-info'),
        ], className='col-md-3 padit'),
        html.Div([
        html.Div([
                html.Div([
                    html.H3("Recovered", className='text-light'),
                    html.H4(RecoveredFigures, className='text-light')
                ], className='card-body')
             ], className='card bg-warning'),
        ], className='col-md-3 padit'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Deaths", className='text-light'),
                    html.H4(DeathsFigures, className='text-light')
                ], className='card-body')
             ], className='card bg-success'),
        ], className='col-md-3 padit')
    ], className='row'),

    html.H3("Country/Region Wise Analysis"),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker', options=options, value=1),
                    dcc.Graph(id='bar')
                ], className='card-body')
            ], className='card')
        ], className='col-md-12')
    ], className='row'),

    html.H3("Cumulative Total Cases, Total deaths and Total Recovered"),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker2', options=options2, value='India'),
                    dcc.Graph(id='line')
                ], className='card-body')
            ], className='card')
        ], className='col-md-12')
    ], className='row'),

    html.H3("Percentage contribution to positive cases of each Country"),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(figure=px.pie(Total,
                                            values=Total.iloc[:,-1],
                                            names='Country/Region',
                                            hover_name='Country/Region',
                                            title='Percentage contribution to positive cases of each Country').update_traces(textposition='inside', textinfo='percent+label'),)
                ], className='card-body')
            ], className='card')
        ], className='cold-md-12', style={'margin': '0 auto'})
    ], className='row'),

    html.H3("Death Trend-Covid 19"),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker3', options=options2, value='India'),
                    dcc.Graph(id='bar1')
                ], className='card-body')
            ], className='card')
        ], className='col-md-12')
    ], className='row'),

    html.H3("Recovery Trend-Covid 19"),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker4', options=options2, value='India'),
                    dcc.Graph(id='bar2')
                ], className='card-body')
            ], className='card')
        ], className='col-md-12')
    ], className='row'),
    html.H3("Tabular representation of COVID-19", style={ 'text-align':'center'}),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        dash_table.DataTable( id='table', columns=[{"name": i, "id":i} for i in Data.columns], data=Data.to_dict('records')),
                    ], className='card-body table-overflow')
                ], className='card')
            ], className='col-md-12')
        ], className='row')
    ], className='container')

@app.callback(Output('bar','figure'), [Input('picker','value')])
def update_graph(type):
    return {
        'data': [
            go.Bar(
                x=Data['Country/Region'],
                y=Data.iloc[:,type]
            )
        ],
        'layout': go.Layout({
            'title': 'Country/Region wise Analysis'}
        )
    }

@app.callback(Output('line', 'figure'), [Input('picker2', 'value')])
def update_graph2(type):
    return {
        'data': [
            go.Scatter(
                x=Dates,
                y=x.get_group(type).sum()[4:],
                marker={'color':'blue'},
                name = "Total Cases"
                ),
            go.Scatter(
                 x=Dates,
                 y=y.get_group(type).sum()[4:],
                marker={'color': 'red'},
                name= "Total Deaths"
                ),
            go.Scatter(
                x=Dates,
                y=z.get_group(type).sum()[4:],
                marker={'color': 'green'},
                name="Total Recoveries"
                )

            ],
        'layout': go.Layout({
                'title': 'Cumulative Total Cases, Total deaths and Total Recovered'}
            )
        }

@app.callback(Output('bar1', 'figure'), [Input('picker3', 'value')])
def update_graph3(type):
    return {
        'data': [
            go.Bar(
                x=Dates,
                y=y.get_group(type).sum()[4:],
                marker={'color': 'red'}
            )
        ],
        'layout': go.Layout({
            'title': 'Death Trend-Covid 19'}
        )
     }

@app.callback(Output('bar2', 'figure'), [Input('picker4', 'value')])
def update_graph4(type):
    return {
        'data': [
            go.Bar(
                x=Dates,
                y=z.get_group(type).sum()[4:],
                marker={'color': 'green'}
            )
        ],
        'layout': go.Layout({
            'title': 'Recovery Trend-Covid 19'}
        )
    }
    # else:
    #     return {
    #         'data': [
    #             go.Bar(
    #                 x=Data['Country/Region'],
    #                 y=Data[type]
    #             )
    #         ],
    #         'layout': go.Layout(title= 'Country/Region wise Analysis')
    #     }


if __name__ == "__main__":
    app.run_server(debug=True)
