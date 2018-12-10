import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime
from pymongo import MongoClient
import pandas as pd
from textwrap import dedent



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

client = MongoClient('mongodb://34.201.135.161/cool_db')
db = client.smartwatch_db
# get the data from the database of a user and display it.

def categorize_time(x):
    if x.hour < 11:
        return 'breakfast'
    if x.hour < 14:
        return 'lunch'
    if x.hour < 18:
        return 'afternoon'
    else:
        return 'dinner'


def calculate_values(db):
    data = pd.DataFrame(list(db.spoondata_user.find()),
                        columns=['timestamp', 'food', 'foodtype', 'weight',
                                 'calories', 'temperature'])
    data['timestamp'] = pd.to_datetime(data.timestamp)
    data['cat'] = data.timestamp.apply(lambda d: categorize_time(d))
    carbs = data[(data.timestamp.dt.date == datetime.datetime.now().date()) &
                 (data.foodtype == 'carbs')].groupby('cat').sum().calories

    protein = data[(data.timestamp.dt.date == datetime.datetime.now().date()) &
                   (data.foodtype == 'protein')].groupby('cat').sum().calories

    veggies = data[(data.timestamp.dt.date == datetime.datetime.now().date()) &
                   (data.foodtype == 'veggie')].groupby('cat').sum().calories

    calories_today = carbs.sum() + protein.sum() + veggies.sum()
    bites = data[(data.timestamp.dt.date ==
                  datetime.datetime.now().date())].shape[0]

    favorite = data.groupby('food').count(). \
        sort_values('timestamp', ascending=True)
    return carbs, protein, veggies, calories_today, bites, favorite


data = pd.DataFrame(list(db.spoondata_user.find()),
                        columns=['timestamp', 'food', 'foodtype', 'weight',
                                 'calories', 'temperature'])
data['timestamp'] = pd.to_datetime(data.timestamp)
data['cat'] = data.timestamp.apply(lambda d: categorize_time(d))


carbs, protein, veggies,\
calories_today, bites, favorite = calculate_values(db)
# calculate all metrics


app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                static_folder='static'
                )


app.layout = html.Div(children=[


    html.Div([
        html.Div([
            html.Div([
                html.H1('Spoony - your Smart Spoon'),
            ], className="six columns"),

            html.Div([
                html.Button('Refresh', id='refresh',n_clicks_timestamp=1),
            ], className="six columns"),
            html.Div([
                html.Button('Reset', id='reset', n_clicks_timestamp=0),
            ], className="six columns"),
        ], className="row")
    ]),
    dcc.Markdown(id='spoon_bites', children=dedent('''
    #### Learn more about your eating habits

    ###### **Your calories today**:
    ### {}
    which has been calculate by {} bites.
    ###### **Your daily recommended calories**
    ### 2760

    '''.format(round(calories_today), bites))),

    dcc.Graph(
        id='food-composition-day',
        figure={
            'data': [
                {'x': ['breakfast', 'lunch', 'afternoon', 'dinner'],
                 'y': [None, None, None, None],
                 'type': 'bar',
                 'name': '',
                 'showlegend': False},
                {'x': veggies.index,
                 'y': veggies.values, 'type': 'bar', 'name': u'veggies'},
                {'x': protein.index,
                 'y': protein.values, 'type': 'bar', 'name': u'protein'},
                {'x': carbs.index,
                 'y': carbs.values,
                 'type': 'bar', 'name': 'carbs'},

            ],
            'layout': {
                'title': 'Your Food today',
                'barmode': 'stack',
                'yaxis': { 'labels': ['breakfast','lunch',
                                      'afternoon','dinner'],
                           'title': 'Calories'},
                'xaxis': {
                    'title': 'Time of day'}
            }
        }
    ),
    dcc.Markdown(dedent('''
     It is recommended, to always eat at the same time of your day, so your
     body can adapt its digestive systems and hormons.

     ''')),
    dcc.Graph(
        id='food-composition',
        figure = {
          "data": [
            {
              "values": data.groupby('foodtype').sum()['calories'],
              "labels": data.foodtype.unique(),
              "domain": {"x": [0, .48]},
              "name": "You",
              "hole": .4,
              "type": "pie",
              "hoverinfo":"label+percent",
              "sort": False
            },
            {
              "values": [49,34,23],
              "labels": data.foodtype.unique(),
              "textposition":"inside",
              "domain": {"x": [.52, 1]},
              "name": "Optimum",
              "hole": .4,
              "type": "pie",
              "hoverinfo":"label+percent",
              "sort": False
            }],
          "layout": {
                "title":"Your food composition last week",
                "sort": "false",
                "annotations": [
                    {
                        "font": {
                            "size": 20
                        },
                        "showarrow": False,
                        "text": "You",
                        "x": 0.20,
                        "y": 0.5
                    },
                    {
                        "font": {
                            "size": 20
                        },
                        "showarrow": False,
                        "text": "Ideal",
                        "x": 0.8,
                        "y": 0.5
                    }
                ]
            }
        }),

    dcc.Markdown(dedent('''
 The left hand graph shows your food composition last week. Compare it to the ideal
  food consumption recommended by health advisors.

 ''')),
    dcc.Graph(
        id='calories-per-day',
        figure={
            'data': [
                {'x': data.timestamp.dt.date.unique(),
                 'y': data.groupby(data.timestamp.dt.day).calories.sum(),
                 'type': 'bar'}

            ],
            'layout': {
                'title': 'Total calories per day',
                'yaxis': {
                    'title': 'Calories'},
                'xaxis': {
                    'title': 'Day'}
            }
        }),
dcc.Markdown(dedent('''
 Check out the days you hit your calorie limit, and where you exceeded it.

 ''')),
    dcc.Graph(
        id='favorite-foods',
        figure={
            'data': [
                {'x': favorite['timestamp'],
                 'y': favorite.index,
                 'type': 'bar',
                 'orientation': 'h'
                 }

            ],
            'layout': {
                'title': 'Your favorite food',
                'barmode': 'stack',
                'xaxis': {
                     'title': 'Number of bites'}
            }
        }
    ),

    dcc.Markdown(dedent(''' Your favorite foods are {},{},{}. Do you think they are good for you?

    #### Share your results with your friends!
    ![share](/static/socmedbar2.png)
'''.format(favorite.index[-1],favorite.index[-2],favorite.index[-3]))),
])


@app.callback(
    dash.dependencies.Output('food-composition-day', 'figure'),
    [dash.dependencies.Input('refresh', 'n_clicks_timestamp'),
     dash.dependencies.Input('reset', 'n_clicks_timestamp')])
def refresh_values1(refresh, reset):
    if reset > refresh:
        db.spoondata_user.delete_many(
            {"timestamp": {"$gt": '2018-12-02 18:00:07.402029'}})
    carbs, protein, veggies, \
    calories_today, bites, favorite = calculate_values(db)
    return {
            'data': [
                {'x': ['breakfast', 'lunch', 'afternoon', 'dinner'],
                 'y': [None, None, None, None],
                 'type': 'bar',
                 'name': '',
                 'showlegend': False},
                {'x': veggies.index,
                 'y': veggies.values, 'type': 'bar', 'name': u'veggies'},
                {'x': protein.index,
                 'y': protein.values, 'type': 'bar', 'name': u'protein'},
                {'x': carbs.index,
                 'y': carbs.values,
                 'type': 'bar', 'name': 'carbs'},

            ],
            'layout': {
                'title': 'Your Food today',
                'barmode': 'stack',
                'yaxis': { 'labels': ['breakfast','lunch',
                                      'afternoon','dinner'],
                           'title': 'Calories'},
                'xaxis': {
                    'title': 'Time of day'}
            }
        }

@app.callback(
    dash.dependencies.Output('spoon_bites', 'children'),
    [dash.dependencies.Input('refresh', 'n_clicks_timestamp'),
     dash.dependencies.Input('reset', 'n_clicks_timestamp')])
def refresh_values2(refresh, reset):
    if reset > refresh:
        db.spoondata_user.delete_many(
            {"timestamp": {"$gt": '2018-12-02 18:00:07.402029'}})
    carbs, protein, veggies, \
    calories_today, bites, favorite = calculate_values(db)
    print('refresh values')
    return dedent('''
    #### Learn more about your eating habits

    ###### **Your calories today**:
    ### {}
    which has been calculate by {} bites.
    ###### **Your daily recommended calories**
    ### 2760

    '''.format(round(calories_today), bites))



if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server(debug=True, host='0.0.0.0', port=80)