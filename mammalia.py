#!/usr/bin/env python
# utf-8


import numpy as np
import pandas as pd
import argparse
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.plotting import show, output_file
from bokeh.charts import BoxPlot, Bar
from bokeh.io import vplot, output_file


# argparse takes in file location, fiile output
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--data_file', required=True, type=str, help='provide the path to the amniote database file.\n Alternatvely, you can use the url\n http://esapubs.org/archive/ecol/E096/269/Data_Files/Amniote_Database_Aug_2015.csv\n but it is slower and requires the internet')
parser.add_argument('-o', '--out_file', required=True, type=str, help='provide the path for the output html file')
args = parser.parse_args()


# import and clean data file
data = pd.read_csv(args.data_file)
data = data[data['class'] == 'Mammalia']
data = data.replace(-999, np.nan)
data = data.replace(-999.00, np.nan)
cols = [0, 1, 2, 3, 4, 10, 28]
data = data[cols]
data.rename(columns={'adult_body_mass_g': 'mass', 'adult_svl_cm':
                     'length'}, inplace=True)


# we can plot family and order from mass_data & length_data
data['log_mass'] = np.log(data.mass)
data['log_length'] = np.log(data.length)
mass_data = data.round({'log_mass': 2})
length_data = data.round({'log_length': 2})


# order mass boxplot
a1 = BoxPlot(mass_data, values='log_mass', label='order', title="Log Mass(g) for Every Order", width=1500, height=600, color='order')


# order mass table
order_group = mass_data.groupby(['order'])
order_mass = order_group.agg(np.mean)
order_mass = order_mass.reset_index()
order_mass = order_mass.round({'mass': 2})

# create table of order mass
source1 = ColumnDataSource(order_mass)
columns1 = [TableColumn(field="order", title="Order"), TableColumn(field="mass", title="Mean Mass(g)")]
a2 = DataTable(source=source1, columns=columns1, width=400, height=600)


# family mass boxplot
c1 = BoxPlot(mass_data, values='log_mass', label='family',
             title="Log Mass(g) for Every Family", width=2500,
             height=600, color='family')


# family mass table
fam_group = mass_data.groupby(['family'])
fam_mass = fam_group.agg(np.mean)
fam_mass = fam_mass.reset_index()
fam_mass = fam_mass.round({'mass': 2})

# create table of family mass
source2 = ColumnDataSource(fam_mass)
columns2 = [TableColumn(field="family", title="Family"), TableColumn(field="mass", title="Mean Mass(g)")]
c2 = DataTable(source=source2, columns=columns2, width=400, height=600)


# Produce order_dif correctly for plotting order disparity
order_dif = data.drop(data.columns[[0, 2, 3, 4, 5, 6, 8]], axis=1)
order_dif = order_dif.groupby(['order'])
order_dif = order_dif.agg([np.amin, np.amax])
order_dif = order_dif.reset_index()
order_dif.columns = [' '.join(col).strip() for col in
                     order_dif.columns.values]
order_dif.rename(columns={'log_mass amin': 'log_mass_min',
                 'log_mass amax': 'log_mass_max'}, inplace=True)
order_dif['dif'] = order_dif['log_mass_max'] - order_dif['log_mass_min']


# plot disparity in orders
b1 = Bar(order_dif, 'order', values='dif',
         title="Disparity in Body Mass by Order (log transformed)",
         bar_width=0.5, width=1500, height=600,
         color='order', agg='mean')



# Produce fam_dif correctly for plotting family disparity
fam_dif = data.drop(data.columns[[0, 1, 3, 4, 5, 6, 8]], axis=1)
fam_dif = fam_dif.groupby(['family'])
fam_dif = fam_dif.agg([np.amin, np.amax])
fam_dif = fam_dif.reset_index()
fam_dif.columns = [' '.join(col).strip() for col in fam_dif.columns.values]
fam_dif.rename(columns={'log_mass amin': 'log_mass_min',
               'log_mass amax': 'log_mass_max'}, inplace=True)
fam_dif['dif'] = fam_dif['log_mass_max'] - fam_dif['log_mass_min']


# plot disparity in family mass
d1 = Bar(fam_dif, 'family', values='dif',
         title="Disparity in Body  Mass by Family (log transformed)",
         width=2500, bar_width=0.5, height=600,
         color='family', agg='mean')


# find 20 families with most disparate mass
top_fams = fam_dif.nlargest(20, "dif")

# plot those 20 families
e1 = Bar(top_fams, 'family', values='dif',
         title="The 20 Families with Most Disparate Mass (log transformed)",
         bar_width=0.7, height=600, width=1000,
         color='family', agg='mean')


# we can plot family and order from length_data
data['log_length'] = np.log(data.length)
length_data = data.round({'log_length': 2})


# order length boxplot
f1 = BoxPlot(length_data, values='log_length', label='order',
             title="Log Length(g) for Every Order", width=1500,
             height=600, color='order')


# order length table
order_group_l = length_data.groupby(['order'])
order_length = order_group_l.agg(np.mean)
order_length = order_length.dropna(axis=0)
order_length = order_length.reset_index()
order_length = order_length.round({'length': 2})
source1 = ColumnDataSource(order_length)
columns1 = [TableColumn(field="order", title="Order"), TableColumn(field="length", title="Mean Length(cm)")]
f2 = DataTable(source=source1, columns=columns1,
               width=400, height=600)


# family length boxplot
h1 = BoxPlot(length_data, values='log_length', label='family',
             title="Log Length(g) for Every Family", width=2500,
             color='family', height=600)


# family length table
fam_group_l = length_data.groupby(['family'])
fam_length = fam_group_l.agg(np.mean)
fam_length = fam_length.dropna(axis=0)
fam_length = fam_length.reset_index()
fam_length = fam_length.round({'length': 2})
source2 = ColumnDataSource(fam_length)
columns2 = [TableColumn(field="family", title="Family"), TableColumn(field="length", title="Mean Length(cm)")]
h2 = DataTable(source=source2, columns=columns2, width=400, height=600)


# Produce order_dif_l correctly for plotting order disparity
order_dif_l = data.drop(data.columns[[0, 2, 3, 4, 5, 6, 7]], axis=1)
order_dif_l = order_dif_l.groupby(['order'])
order_dif_l = order_dif_l.agg([np.amin, np.amax])
order_dif_l = order_dif_l.reset_index()
order_dif_l.columns = [' '.join(col).strip() for col in order_dif_l.columns.values]
order_dif_l.rename(columns={'log_length amin': 'log_length_min',
                   'log_length amax': 'log_length_max'},
                   inplace=True)
order_dif_l['dif'] = order_dif_l['log_length_max'] - order_dif_l['log_length_min']


# plot disparity in orders
g1 = Bar(order_dif_l, 'order', values='dif',
         title="Disparity in Body Length by Order (log transformed)",
         bar_width=0.5, width=1500, color='order', agg='mean')


# Produce fam_dif correctly for plotting family disparity
fam_dif_l = data.drop(data.columns[[0, 1, 3, 4, 5, 6, 7]], axis=1)
fam_dif_l = fam_dif_l.groupby(['family'])
fam_dif_l = fam_dif_l.agg([np.amin, np.amax])
fam_dif_l = fam_dif_l.reset_index()
fam_dif_l.columns = [' '.join(col).strip() for col in fam_dif_l.columns.values]
fam_dif_l.rename(columns={'log_length amin': 'log_length_min',
                 'log_length amax': 'log_length_max'}, inplace=True)
fam_dif_l['dif'] = fam_dif_l['log_length_max'] - fam_dif_l['log_length_min']


# plot disparity in family length
i1 = Bar(fam_dif_l, 'family', values='dif',
         title="Disparity in Body Length by Family (log transformed)",
         width=2500, bar_width=0.5, color='family',
         agg='mean', height=600)


# find the 20 families with the most disparate length
top_fams_l = fam_dif_l.nlargest(20, "dif")


# plot the 20 most disparate
j1 = Bar(top_fams_l, 'family', values='dif',
         title="The 20 Families with Most Disparate Body Length (log transformed)",
         bar_width=0.7, width=1000, color='family',
         agg='mean', height=600)

output_file(args.out_file)

show(vplot(a1, a2, b1, c1, c2, d1, e1, f1, f2, g1, h1, h2, i1, j1))
