# In[]
# importing simulator functions and all dependencies
__name__ = "Simulator"
__version__ = "6.01.00.2020"
import plotly.offline as py
import plotly
import plotly.io as pio
import plotly.express as px
import cufflinks as cf
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly import graph_objs as go

import matplotlib.pyplot as plt
# %matplotlib inline
py.init_notebook_mode(connected=True)

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

import SD as sd  # builtin functions for system dynamics
import random

from scipy.signal import chirp, find_peaks, peak_widths
import numpy as np
from datetime import date
import time
import os

developer = "(c) 2020, Anupam Saraph"
notice = "This work is licensed under a \nCreative Commons Attribution-NonCommercial 4.0 Unported License \nhttp://creativecommons.org/licenses/by-nc/4.0/"
__doc__ = "Model simulator and output functions common to all models"

# Add only add functions that are model independent here

Scenarios = {}  # create an empty dictionary of scenarios
Describe = {}  # create an empty dictionalry to contain as value dictionary of variables for each scenario as key
PeakStatistic = {}  # create an empty dictionary of statistics about peak for every scenario
# description = {}  # create an empty dictionary of scenario parameters
scenario = ""
path = ""
verbose = False
show = False
save = False
# In[]
# the function to simulate the model over the time period


def reset(ver):
    """
    reset [reset all scenario data structures]

    [reset the dictionary of scenarios and parameter descriptions
    and peak statistics.
    create a path to store all output in a folder named after the model version]

    Args:
        ver ([string]): [version number of the model]
    """    
    global Scenarios, Describe, PeakStatistic, description, path
    print(__name__+" Version " + __version__ +
          "\n" + developer + "\n" + notice)
    Scenarios = {}
    Describe = {}
    PeakStatistic = {}
    description = {}

    if not os.path.exists(ver):
        os.mkdir(ver)
    path = ver + "/"
    

def simulate(model, model_name, scenario, no_of_time_points, dt):
    """
    simulate [function to invoke the model equations from starttime to endtime]

    [extended_summary]

    Args:
        model ([function]): [the function with model equations]
        model_name ([string]): [the name of the model being simulated]
        scenario ([string]): [the name of the scenario being simulated]
        no_of_time_points ([integer]): [the number of iterations for simulation]
        dt ([float]): [the time interval between each iteration]
    """
    global current_time
    start = time.time()
    for t in range(no_of_time_points):  # Integration
        # Create array indices for past, present and future
        j = t - 1  # past
        k = t  # present
        jk = t - 1  # interval between past and present
        kl = t  # interval between present and future
        current_time = t/dt
        model(t, dt, j, k, jk, kl)
    end = time.time()
    if verbose:
        print("simulation of ", model_name, " scenario ",
              scenario, " for ", no_of_time_points*dt, " days "
              " took "+str(end-start)+" seconds")


# In[]
# Output functions


def list_scenarios():
    return Scenarios.keys()


def describe_scenarios():
    description = ""
    for key in Scenarios.keys():
        description = description + str(key) + ""
        for k in Describe[key].keys():
            description = description + k + \
                " : " + str(Describe[key][k]) + ""
    description + ""
    return description


def describe_scenario(scenario):
    return scenario, Describe[scenario]


def print_scenario_parameters(scenario):
    description = ""
    description = description + str(scenario) + ""
    for k in Describe[scenario].keys():
        description = description + k + \
            " : " + str(Describe[scenario][k]) + ""
    description + ""
    return description


def describe():
    scenario_description_list = []
    for key in Scenarios.keys():
        for k in Describe[key].keys():
            scenario_description_list.append((key, k, Describe[key][k]))
    return pd.DataFrame(scenario_description_list, columns=['scenario', 'parameter', 'value'])


def describe_peaks():
    # prepare the data for ploting by merging the dataframes
    df = pd.concat(PeakStatistic.values(), keys=PeakStatistic.keys(),
                   names=['scenario', 'no'])
    # convert the multiindex to columns for plot to work
    df.reset_index(inplace=True)
    return df


def describe_peak(scenario):
    return scenario, PeakStatistic[scenario]


def store_scenario(scenario, df, description, dt):
    # add the dataframe as value with scenario name as key in a dictionary
    Scenarios[scenario] = df
    Describe[scenario] = description
    #PeakStatistic[scenario] = peak_statistics(df, dt)
    return Scenarios[scenario]


def get_run_data():
    # prepare the data for ploting by merging the dataframes
    df = pd.concat(Scenarios.values(), keys=Scenarios.keys(),
                   names=['scenario', 'no'])
    # convert the multiindex to columns for plot to work
    df.reset_index(inplace=True)
    return df


def summarize(y, scenario_parameter,dt):
    df = pd.DataFrame()
    max_y = {}
    time_max_y = {}
    parameter = {}
    for key in Scenarios:
        parameter[key] = Describe[key][scenario_parameter][1]
        max_y[key] = Scenarios[key][y].max()
        time_max_y[key] = Scenarios[key][Scenarios[key]
                                            [y] == max_y[key]].index[0]*dt
    df1 = pd.Series(parameter)
    df2 = pd.Series(max_y)
    df3 = pd.Series(time_max_y)
    df = pd.concat([df1, df2, df3], axis=1)
    df.columns = [scenario_parameter, 'peak', 'peak_time']
    df.index.names = ['scenario']
    return df


def peak_statistics(df, dt):
    list_of_column_names = []
    list_of_peak_start = []
    list_of_peak_end = []
    list_of_peak_height = []
    list_of_peak_duration = []

    for column in df.columns:
        if column != 'scenario' and column != 'time' and column != 'no':

            peaks, _ = find_peaks(df[column])
            peak_data = peak_widths(df[column], peaks, rel_height=1)
            list_of_column_names.append(column)
            try:
                list_of_peak_start.append(peak_data[2][0]*dt)
                list_of_peak_end.append(peak_data[3][0]*dt)
                list_of_peak_height.append(peak_data[1][0])
                list_of_peak_duration.append(peak_data[0][0]*dt)
            except:
                list_of_peak_start.append(0)
                list_of_peak_end.append(0)
                list_of_peak_height.append(0)
                list_of_peak_duration.append(0)
        statistics = [list_of_peak_start, list_of_peak_end,
                      list_of_peak_height, list_of_peak_duration]
        statistic = zip(list_of_peak_start, list_of_peak_end,
                        list_of_peak_height, list_of_peak_duration)
        df1 = pd.DataFrame(statistic, index=list_of_column_names, columns=[
            'peak_start', 'peak_end', 'peak_height', 'peak_duration'])

        df1.fillna(0, inplace=True)

    return df1

# In[]
# functions for plotting variables

def save_file(filename, fig, y):
    global path
    if save == True:
        today = str(date.today())
        file = path + today + " - " + filename + "-" + y
        print('writing file ', file)
        fig.write_image(file + ".svg")
        fig.write_html(file + ".html")


def reference_plot(df_y, df_reference, y, reference, xtitle, ytitle, title, filename):
    pio.templates.default = "simple_white+gridon"
    fig = px.line(df_y, x='time', y=y, title=title,
                  color='scenario', width=800)

    fig.add_trace(
        go.Scatter(
            x=df_reference['time'],
            y=df_reference[reference],
            mode="lines",
            line=go.scatter.Line(color="red"),
            name='historical data',
            showlegend=True)
    )

    fig.update_xaxes(title_text=xtitle)
    fig.update_yaxes(title_text=ytitle)
    fig.update_layout(legend_orientation="h")

    # fig.add_annotation(text='historical data',x=100,y=1000)
    if show == True:
        fig.show()
    save_file(filename, fig, y)


def plot_reference(y, c, title, xtitle, ytitle, annotation, filename):
    # plot x vs y using plotly express
    df = get_run_data()
    pio.templates.default = "simple_white+gridon"
    fig = px.line(df, x='time', y=y, title=title, width=800,
                  color='scenario', hover_data=['time'])
    fig.add_shape(  # add a horizontal "target" line
        type="line", line_color="red", line_width=3, opacity=1, line_dash="dot",
        x0=0, x1=1, xref="paper", y0=c, y1=c, yref="y", fillcolor="LightSalmon")

    fig.update_xaxes(title_text=xtitle)
    fig.update_yaxes(title_text=ytitle)

    fig.add_annotation(  # add a text callout
        text=annotation, x=0, y=c)
    fig.update_traces(textposition='top center')
    fig.update_layout(
        height=800,
    )
    if show == True:
        fig.show()
    save_file(filename, fig, y)


def plotx(y, title, filename):
    # plot y vs time using plotly express
    df = get_run_data()
    pio.templates.default = "simple_white+gridon"
    fig = px.line(df, x="time", y=y, title=title, color='scenario')
    if show == True:
        fig.show()
    save_file(filename, fig, y)


# def plotz(z):
#     # plot z vs time using plotly express
#     df = get_run_data()
#     pio.templates.default = "simple_white+gridon"
#     fig = px.bar(df, x="time", y=z, color='scenario')
#     fig.show()


def plotxy(x, y, title, xtitle, ytitle, filename):
    # plot x vs y using plotly express
    df = get_run_data()
    pio.templates.default = "simple_white+gridon"
    fig = px.scatter(df, x=x, y=y, color='scenario',
                     height=800, title=title, hover_data=['time'])
    # fig.update_layout(height=800)
    fig.update_xaxes(title_text=xtitle)
    fig.update_yaxes(title_text=ytitle)
    fig.update_layout(legend_orientation="h")

    if show == True:
        fig.show()
    save_file(filename, fig, y)


def plot_log_y(y, title, xtitle, ytitle, filename):
    # plot x vs y using plotly express
    df = get_run_data()
    pio.templates.default = "simple_white+gridon"
    fig = px.line(df, x='time', y=y, title=title, width=800, log_y=True,
                  color='scenario', hover_data=[y])
    fig.update_xaxes(title_text=xtitle)
    fig.update_yaxes(title_text=ytitle)
    fig.update_layout(legend_orientation="h")
    fig.update_layout(showlegend=False)
    if show == True:
        fig.show()
    save_file(filename, fig, y)


def plotx_logy(x, y, title, xtitle, ytitle, filename):
    # plot x vs y using plotly express
    df = get_run_data()
    pio.templates.default = "simple_white+gridon"
    fig = px.scatter(df, x=x, y=y, color='scenario', log_y=True, width=800,
                     title=title, hover_data=[y])
    fig.update_xaxes(title_text=xtitle)
    fig.update_yaxes(title_text=ytitle)
    fig.update_layout(legend_orientation="h")
    fig.update_layout(showlegend=True)
    if show == True:
        fig.show()
    save_file(filename, fig, y)

def plot_x_log_y(df, x, y, title, xtitle, ytitle, filename, legend):
    # plot x vs y using plotly express
    pio.templates.default = "simple_white+gridon"
    fig = px.scatter(df, x=x, y=y, color='scenario', log_y=True, width=800,
                     title=title, hover_data=[y])
    fig.update_xaxes(title_text=xtitle)
    fig.update_yaxes(title_text=ytitle)
    #fig.update_layout(legend_orientation="h")
    fig.update_layout(showlegend=legend)
    if show == True:
        fig.show()
    save_file(filename, fig, y)

def ploty(y, title, xtitle, ytitle, filename):
    # plot x vs y using plotly express
    df = get_run_data()
    pio.templates.default = "simple_white+gridon"
    fig = px.line(df, x='time', y=y, title=title, width=800,
                  color='scenario', hover_data=['time'])
    fig.update_xaxes(title_text=xtitle)
    fig.update_yaxes(title_text=ytitle)
    #fig.update_layout(legend_orientation="h")
    fig.update_layout(showlegend=False)
    if show == True:
        fig.show()
    save_file(filename, fig, y)


def plotsc(y, scenario, title, xtitle, ytitle, filename):
    # plot y vs time using plotly express
    df = get_run_data()
    pio.templates.default = "simple_white+gridon"
    fig = px.line(df, x="time", y=y, color='scenario', height=400, width=800, title=title,
                  line_group=scenario, facet_col=scenario)
    # fig.update_layout(height=400, width=800, title_text=title)
    fig.update_xaxes(title_text=xtitle)
    fig.update_yaxes(title_text=ytitle)
    fig.update_layout(legend_orientation="h")
    if show == True:
        fig.show()
    save_file(filename, fig, y)


def plotsr(y, scenario, title, xtitle, ytitle, filename):
    # plot y vs time using plotly express
    df = get_run_data()
    pio.templates.default = "simple_white+gridon"
    fig = px.line(df, x="time", y=y, color='scenario', height=800, width=700, title=title,
                  line_group=scenario, facet_row=scenario)
    # fig.update_layout(height=800, width=700, title_text=title)
    fig.update_xaxes(title_text=xtitle)
    fig.update_yaxes(title_text=ytitle)
    fig.update_layout(legend_orientation="h")

    if show == True:
        fig.show()
    save_file(filename, fig, y)


def plotpeak(x, y, title, xtitle, ytitle, filename):
    # plot y vs time using plotly express
    df = describe_peaks()
    pio.templates.default = "simple_white+gridon"
    fig = px.line(df, x=x, y=y, title=title, color='scenario')
    fig.update_xaxes(title_text=xtitle)
    fig.update_yaxes(title_text=ytitle)
    fig.update_layout(legend_orientation="h")
    if show == True:
        fig.show()
    save_file(filename, fig, y)


def plotpeakxy(x, y, title, xtitle, ytitle, filename):
    # plot x vs y using plotly express
    df = describe_peaks()
    pio.templates.default = "simple_white+gridon"
    fig = px.line(df, x=x, y=y, color='scenario', title=title)
    fig.update_xaxes(title_text=xtitle)
    fig.update_yaxes(title_text=ytitle)
    fig.update_layout(legend_orientation="h")
    if show == True:
        fig.show()
    save_file(filename, fig, y)


# def mplot(scenario, y):
#     # plot x vs time using mathplot
#     fig, ax = plt.subplots()
#     ax.set_xlabel('time')
#     ax.set_ylabel(str(y))
#     ax.set_title(scenario)
#     ax.plot(range(no_of_time_points), y)


# def mplotxy(scenario, x, y):
#     # plot x vs y using mathplot
#     fig, ax = plt.subplots()
#     ax.set_xlabel(str(x))
#     ax.set_ylabel(str(y))
#     ax.plot(x, y)
#     ax.annotate(scenario, xy=(3, 1),  xycoords='data',
#                 xytext=(0.8, 0.95), textcoords='axes fraction',
#                 arrowprops=dict(facecolor='black', shrink=0.05),
#                 horizontalalignment='right', verticalalignment='top')

def save_to_csv(df, y, filename, mode):
    global path
    today = str(date.today())
    filename = path + today + " - " + filename +  " - " + str(y)
    print("writing to filename: ", filename)
    df.save_to_csv(filename)
    return filename


def save_to_excel(df, y, filename, mode):
    global path
    today = str(date.today())
    filename = path + today + " - " + filename +  " - " + str(y)
    print("writing to filename: ", filename)
    writer = ExcelWriter(filename + ".xlsx", engine='openpyxl', mode=mode)
    df.to_excel(writer, sheet_name=y)
    writer.save()


def compare_scenarios_to_excel(filename):
    global path
    # write all the scenarios to a single excel sheet
    today = str(date.today())
    filename = path + today + " - " + filename
    print("writing to filename: ", filename)

    writer = ExcelWriter(filename)

    describe().to_excel(writer, sheet_name='Scenario List')

    df = get_run_data()
    # aggregate all scenario values for each variable
    # write aggregared values of each variable into different worksheet
    for col in df.columns:
        if col != 'scenario' and col != 'time' and col != 'no':
            data = pd.pivot_table(df, values=col, index=[
                                  'time'], columns=['scenario'])
            data.to_excel(writer, sheet_name=col)

    # aggregate all scenario values for each peak statistic
    # write aggregated peak statistics into different worksheet
    # df1 = describe_peaks()
    # # try:
    # peak_start = pd.pivot_table(df1, values='peak_start', index=[
    #     'no'], columns=['scenario'])
    # peak_end = pd.pivot_table(df1, values='peak_end', index=[
    #     'no'], columns=['scenario'])
    # peak_height = pd.pivot_table(df1, values='peak_height', index=[
    #     'no'], columns=['scenario'])
    # peak_duration = pd.pivot_table(df1, values='peak_duration', index=[
    #     'no'], columns=['scenario'])
    # # except:
    # #    print("some non numeric values")

    # peak_start.to_excel(writer, sheet_name="peak_start")
    # peak_end.to_excel(writer, sheet_name="peak_end")
    # peak_height.to_excel(writer, sheet_name="peak_height")
    # peak_duration.to_excel(writer, sheet_name="peak_duration")

    writer.save()


# %%


# %%
