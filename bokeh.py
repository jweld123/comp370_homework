import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure

data = pd.read_csv('nyc_2020.csv')

data['month'] = pd.to_datetime(data['month'].astype(str))

def get_zipcode_data(zipcode):
    return data[data['zipcode'] == int(zipcode)]

source_all = ColumnDataSource(data.groupby('month')['response_time_hours'].mean().reset_index())
source_zip1 = ColumnDataSource(get_zipcode_data(10001))
source_zip2 = ColumnDataSource(get_zipcode_data(10002))

p = figure(x_axis_type='datetime', title="Monthly Average Response Time", plot_height=400, plot_width=700)
p.line('month', 'response_time_hours', source=source_all, legend_label='All 2020', color='blue', line_width=2)
p.line('month', 'response_time_hours', source=source_zip1, legend_label='Zipcode 1', color='green', line_width=2)
p.line('month', 'response_time_hours', source=source_zip2, legend_label='Zipcode 2', color='red', line_width=2)

p.legend.title = "Data"
p.xaxis.axis_label = "Month"
p.yaxis.axis_label = "Response Time (Hours)"

zipcodes = data['zipcode'].unique().astype(str).tolist()

dropdown_zip1 = Select(title="Select Zipcode 1", value='10001', options=zipcodes)
dropdown_zip2 = Select(title="Select Zipcode 2", value='10002', options=zipcodes)

def update_plot(attr, old, new):
    new_zip1 = get_zipcode_data(dropdown_zip1.value)
    new_zip2 = get_zipcode_data(dropdown_zip2.value)
    
    source_zip1.data = ColumnDataSource(new_zip1).data
    source_zip2.data = ColumnDataSource(new_zip2).data

dropdown_zip1.on_change('value', update_plot)
dropdown_zip2.on_change('value', update_plot)

layout = column(dropdown_zip1, dropdown_zip2, p)
curdoc().add_root(layout)
curdoc().title = "NYC 311 Dashboard"

curdoc().theme = 'light_minimal'
