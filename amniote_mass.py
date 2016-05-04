#!/usr/bin/env python
# utf-8

import numpy as np
import pandas as pd
import argparse
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.plotting import show, output_file
from bokeh.charts import BoxPlot, Bar, output_file, show
from bokeh.io import vplot, output_file, show



# argparse takes in file location, fiile output, and taxon 'class'
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--data_file', required=True, type=str, help='provide the path to the amniote database file.\n Alternatvely, you can use the url\n http://esapubs.org/archive/ecol/E096/269/Data_Files/Amniote_Database_Aug_2015.csv\n but it is slower and requires the internet')
parser.add_argument('-o', '--out_file', required=True, type=str, help='provide the path for the output html file')
parser.add_argument('-c', '--taxon_class', required=True, type=str, help='mammalia, reptilia, or aves')
args = parser.parse_args()


# import and clean data file
data = pd.read_csv(args.data_file)
data = data[data['class'] == args.taxon_class]
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
             title="Log Mass(g) for Every Family", width=3500,
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
         width=3500, bar_width=0.5, height=600,
         color='family', agg='mean')


# find 20 families with most disparate mass
top_fams = fam_dif.nlargest(20, "dif")

# plot those 20 families
e1 = Bar(top_fams, 'family', values='dif',
         title="The 20 Families with Most Disparate Mass (log transformed)",
         bar_width=0.7, height=600, width=1000,
         color='family', agg='mean')

output_file(args.out_file)

show(vplot(a1,a2,b1,c1,c2,d1,e1))
