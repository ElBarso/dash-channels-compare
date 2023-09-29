import pandas as pd
import numpy as np
from scipy.io import loadmat
import os
import dash
from dash import dcc
from dash import html
from dash import Output, Input, State
import plotly.graph_objs as go
import plotly.offline as pyo
import re


def tag_id(string, reg_exp=r'\('):
    """

    :param reg_exp: The regular expression applied for the string split.
    :type reg_exp: regular expression.
    :param string: The String to split according to the regular expression passed.
    :type string:  String to split using regular expression reg_exp.
    :return: Measurement identification tag.
    It is the first element of the match object obtained after split.
    Equivalent to re.split(reg_exp , string)[0]
    :rtype: String -
    """
    match = re.split(reg_exp, string)
    return match[0]


def load_files(input_path, file_extension):
    tags_list = []
    measures = []
    count = 0

    # Iteratively search along input_path for files with the desired 
    # file_extention and load them in a pandas dataframe
    for root, dirs, files in os.walk(input_path):

        for file in [f for f in files if f.endswith(file_extension)]:
            data_tmp = loadmat(os.path.join(root, file))
            tmp_tag = tag_id(file)

            if tmp_tag not in tags_list:
                tags_list.append(tmp_tag)

            else:
                pass

            df_loaded = pd.DataFrame(data_tmp['meas_plot_array']).transpose()

            # remove unuseful column containing motor position info
            df_loaded.drop(4, axis=1, inplace=True)

            # Add and 'id' curve for identification
            dim = len(df_loaded.iloc[:, 1])
            df_loaded['id'] = count * np.ones(dim)

            # Add 'tag' column containing measurement tag identificator
            # previously extracted from measurement name after load
            df_loaded['tag'] = tmp_tag

            # insert 'time' column containing time (in seconds)
            time = np.array(range(0, dim))
            df_loaded['time'] = time

            #  Append the curve to a list containing all loaded measurements as Pandas DataFrame
            measures.append(pd.DataFrame(df_loaded))

            count = count + 1

    print('\n Loaded {} measurements with extention {}.\n'.format(len(measures), file_extension))

    # Create dictionary with unique 'curve tags values' as keys
    # and different colors as values
    # Used to group same tag measurements when plotting
    tagToColor_dict = {}

    for num, vtag in enumerate(set(tags_list)):
        tagToColor_dict[str(vtag)] = num

    # colors = ['CornflowerBlue', 'Crimson', 'LimeGreen', 'Black', 'mediumpurple',]
    colors = ['mediumaquamarine', 'orangered', 'royalblue', 'blueviolet' ,  'darkturquoise']

    for key, color in zip(tagToColor_dict.keys(), colors[:len(tagToColor_dict.keys())]):
        tagToColor_dict[key] = color

    return measures, tagToColor_dict


def webapp_creator(measures, tagToColor_dict):

    # Create empty lists, one for each data channel
    # Then fill them with dcc graph objects of loaded curves
    ch1 = []
    ch2 = []
    ch3 = []
    ch4 = []


    # Clean curve names for more readable legend and store them in a dictionary
    # The dictionary is accessed when filling legends in graph passing
    # the raw curve tag
    legend_names = {}
    for name in tagToColor_dict.keys():
        if name[-1:] == '_':
            legend_names[str(name)] = name[:-1]
        else:
            legend_names[str(name)] = name

    # Create a graph for each channel containing all the measurements
    for meas in measures:
        for channel in range(4):
            if channel == 0:
                ch1.append(go.Scatter(x=meas['time'],
                                      y=meas.iloc[:, channel],
                                      mode='lines',
                                      name='# ' + str(int(meas['id'][0] + 1)) + ' ' + legend_names[meas['tag'][0]],
                                      line={'width': 2, 'color': tagToColor_dict[meas['tag'][0]]}
                                      ))
            elif channel == 1:
                ch2.append(go.Scatter(x=meas['time'],
                                      y=meas.iloc[:, channel],
                                      mode='lines',
                                      name='# ' + str(int(meas['id'][0] + 1)) + ' ' + legend_names[meas['tag'][0]],
                                      line={'width': 2, 'color': tagToColor_dict[meas['tag'][0]]}
                                      ))
            elif channel == 2:
                ch3.append(go.Scatter(x=meas['time'],
                                      y=meas.iloc[:, channel],
                                      mode='lines',
                                      name='# ' + str(int(meas['id'][0] + 1)) + ' ' + legend_names[meas['tag'][0]],
                                      line={'width': 2, 'color': tagToColor_dict[meas['tag'][0]]}
                                      ))
            elif channel == 3:
                ch4.append(go.Scatter(x=meas['time'],
                                      y=meas.iloc[:, channel],
                                      mode='lines',
                                      name='# ' + str(int(meas['id'][0] + 1)) + ' ' + legend_names[meas['tag'][0]],
                                      line={'width': 2, 'color': tagToColor_dict[meas['tag'][0]]},
                                      #hoverinfo='name'
                                      ))


    # Create a dash web app and fill it with graph objects previously created for each channel
    # The page layout is defined here
    webapp = dash.Dash()

    plot_bgcolor = 'white'
    paper_bgcolor = 'white'
    # plot_bgcolor = 'ivory'
    # paper_bgcolor = 'aliceblue'
    

    webapp.layout = html.Div([
        # Graphs container #1: START
        html.Div([
            html.Div([
                dcc.Graph(id='ch1',
                          figure={
                              'data': ch1,
                              'layout': go.Layout(title='Channel 1', hovermode='closest', plot_bgcolor=plot_bgcolor, paper_bgcolor=paper_bgcolor)
                        #   })], style={'width': '50%', 'height': 200, 'display': 'inline-block'}),
                          })], style={'display': 'inline-block'}),
            html.Div([
                dcc.Graph(id='ch2',
                          figure={
                              'data': ch2,
                              'layout': go.Layout(title='Channel 2', hovermode='closest', plot_bgcolor=plot_bgcolor, paper_bgcolor=paper_bgcolor)
                          #})], style={'width': '50%', 'height': 200, 'display': 'inline-block'})
                          })], style={'display': 'inline-block'})
            ], style={'height': 400}),
        # Graphs container #1: END

        # Graphs container #2: START
        html.Div([
            html.Div([
                dcc.Graph(id='ch3',
                          figure={
                              'data': ch3,
                              'layout': go.Layout(title='Channel 3', hovermode='closest', plot_bgcolor=plot_bgcolor, paper_bgcolor=paper_bgcolor)
                          #})], style={'width': '50%', 'height': 200, 'display': 'inline-block'}),
                          })], style={'display': 'inline-block'}),
            html.Div([
                dcc.Graph(id='ch4',
                          figure={
                              'data': ch4,
                              'layout': go.Layout(title='Channel 4', hovermode='closest', plot_bgcolor=plot_bgcolor, paper_bgcolor=paper_bgcolor)
                          #})], style={'width': '50%', 'height': 200, 'display': 'inline-block'}),
                          })], style={'display': 'inline-block'})
            ], style={'height': 400}),
        # Graphs container #2: END

        # Curve selection container: START
        html.Pre("""
        
        """),
        html.Div([
            html.Div([
                dcc.Dropdown(id='selected-list',
                             options=[
                                 {'label': 'Select curves by clicking on graphs',
                                  'value': None
                                  }],
                             multi=True,
                             value=None
                             )
            ], style={'width': '20%'}),
        ]),
        html.Pre([]),
        html.Div([
            html.Div(id='instructions-head',
                                    children='Curve comparison: \n',
                                    style={'padding': '10px 20px',
                                           'text-transform': 'uppercase',
                                           'font-weight': 'bold',
                                           'font-size': 16,
                                           'background-color': 'ghostwhite'}
                                    ),
                           html.Div(id='instructions-body',
                                    children=[
                                        'To initialize: select one curve for each channel graph by clicking on it.',
                                        html.Pre(),
                                        'Then output will automatically update after each new curve selection.'],
                                    style={'padding': '10px 20px',
                                           'font-size': 16,
                                           'background-color': 'ghostwhite'}
                                    )
        ], style={'width': '20%','display':'inline-block','vertical-align': 'top'}),
            html.Div([
                dcc.Graph(id='selected-graph',
                          figure={'data': [go.Scatter(x=[0, 1],
                                                      y=[0, 1],
                                                      )],
                                  'layout': go.Layout(title='Example Curve: click on curves to compare')}
                          )], style={'width': 850, 'display': 'inline-block', 'vertical-align': 'top'})
            ], style={'display': 'inline-block'})
            # Curve selection container: END


    @webapp.callback(Output('selected-list', 'value'),
                     [Input('ch1', 'clickData'),
                      Input('ch2', 'clickData'),
                      Input('ch3', 'clickData'),
                     Input('ch4', 'clickData')])
    def update_Dropdown(hoverData1, hoverData2, hoverData3, hoverData4):

        # Extract clickData info from Inputs for each channel
        sel_ch1 = int(hoverData1['points'][0]['curveNumber'])
        sel_ch2 = int(hoverData2['points'][0]['curveNumber'])
        sel_ch3 = int(hoverData3['points'][0]['curveNumber'])
        sel_ch4 = int(hoverData4['points'][0]['curveNumber'])

        # Create a value object containing extracted info an pass it ti the dash component
        # to update it using selected info
        # Finally a list containing one dictionary for each channel is returned
        # Each dictionary contains a 'label' for the curve tag name
        # and a 'value' with a dictionary containin x and y data of each curve
        value = [{'label': '# ' + str(sel_ch1 + 1) + ' ' + legend_names[str(measures[sel_ch1]['tag'][0])],
                  'value': {'x': measures[sel_ch1]['time'], 'y':measures[sel_ch1][0]}},
                 
                 {'label': '# ' + str(sel_ch2 + 1) + ' ' + legend_names[str(measures[sel_ch2]['tag'][0])],
                  'value': {'x': measures[sel_ch2]['time'], 'y': measures[sel_ch2][1]}},
                 
                 {'label': '# ' + str(sel_ch3 + 1) + ' ' + legend_names[str(measures[sel_ch3]['tag'][0])],
                  'value': {'x': measures[sel_ch3]['time'], 'y': measures[sel_ch3][2]}},
                 
                 {'label': '# ' + str(sel_ch4 + 1) + ' ' + legend_names[str(measures[sel_ch4]['tag'][0])],
                  'value': {'x': measures[sel_ch4]['time'], 'y': measures[sel_ch4][3]}}
                 ]

        return value


    # @webapp.callback(Output('selections-comparisons', 'figure'),
    #                  [Input('ch1', 'clickData'), Input('ch3', 'clickData')])

    @webapp.callback(Output('selected-graph', 'figure'),
                     [Input('selected-list', 'value')])
    def update_graph_comparison(hoverData):
        # Pint(hoverData1) # return a list containing dictionaries
        # each dictionary correspond to a channel in order of appearance
        # such as, position 0 for ch1, till position 3 for channel 4
        # The dictionary structure is: 'label':String Label and 'value':dict(x=TIME,y=CURVE)
        # print(hoverData)

        # Extract selected curves info and store them

        #CH1 selection
        x_ch1 = hoverData[0]['value']['x']
        y_ch1 = hoverData[0]['value']['y']
        tag_ch1 = hoverData[0]['label']

        # CH2 selection
        x_ch2 = hoverData[1]['value']['x']
        y_ch2 = hoverData[1]['value']['y']
        tag_ch2 = hoverData[1]['label']

        # CH3 selection
        x_ch3 = hoverData[2]['value']['x']
        y_ch3 = hoverData[2]['value']['y']
        tag_ch3 = hoverData[2]['label']

        # CH4 selection
        x_ch4 = hoverData[3]['value']['x']
        y_ch4 = hoverData[3]['value']['y']
        tag_ch4 = hoverData[3]['label']

        # Create a new figure object to update dash graph component
        # with selected curves in order to visually compare them
        LINE_WIDTH = 5
        figure = {'data':[go.Scatter(x=x_ch1,
                                     y=y_ch1,
                                     name='CH1 ' + tag_ch1,
                                     mode='lines',
                                     line={'width': LINE_WIDTH}
                                     ),
                          go.Scatter(x=x_ch2,
                                     y=y_ch2,
                                     name='CH2 ' + tag_ch2,
                                     mode='lines',
                                     line={'width': LINE_WIDTH}
                                     ),
                          go.Scatter(x=x_ch3,
                                     y=y_ch3,
                                     name='CH3 ' + tag_ch3,
                                     mode='lines',
                                     line={'width': LINE_WIDTH}
                                     ),
                          go.Scatter(x=x_ch4,
                                     y=y_ch4,
                                     name='CH4 ' + tag_ch4,
                                     mode='lines',
                                     line={'width': LINE_WIDTH}
                                     )
                          ],
                  'layout': go.Layout(title='Curve comparison')
                  }
        
        return figure

    return webapp


if __name__ == '__main__':

    # extension and folder path of the files to plot
    file_extension = ".mat"
    input_path = r"C:\Users\j.barsotti\Downloads\BeadsData\2022-01-20"
    # input_path = r"C:\Users\j.barsotti\Downloads"

    # Load the files to plot and return plotly.Graph_Objects and a dictionary containing loaded file info
    # used to set up the plot layout
    measures, tagToColor_dictionary = load_files(input_path, file_extension)

    # Create the dash web app, fill it with contents to plot and set the page layout
    # The lunch the server
    webapp = webapp_creator(measures, tagToColor_dictionary)
    webapp.run_server(port=os.getenv("PORT", "9999"))
