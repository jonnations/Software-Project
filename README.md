# Software-Project

## Introduction:
These two programs use data from the Amniote Life History Database (N.P. Myhrvold et al. Ecology 96: 3109) to investigate the differences in both mass and body size between different orders and families of mammals, birds, and reptiles. This outputs to a series of boxplots, tables, and bargraphs in `.html` format. 

## Requirements:
There are two programs available: ```Mammalia.py``` and ```amniote_mass.py```. Both of these require python 3.5 and Anaconda, which is available at <https://www.continuum.io/downloads>. There are several modules to import, and Anaconda makes this easy. 

To install bokeh, the visualization package, please run ```conda install bokeh``` in Anaconda.

This also requires the Amniote Life History Database as an input file. It is available at <http://esapubs.org/archive/ecol/E096/269/#data> under the name `Amniote_Database_Aug_2015.csv`. 

## Use:
There are two programs available: ```Mammalia.py``` and ```amniote_mass.py```:

```Mammalia.py```takes the class Mammalia from the database and outputs several statistics on body mass and body length in an html format. There are **two flags** for this program:

```-d, --data_file```: This is the path where the Amniote Life History Database is located. Alternatively, the operator can put the website <http://esapubs.org/archive/ecol/E096/269/Data_Files/Amniote_Database_Aug_2015.csv> into this flag. However, I recommend that you download the file onto a machine, as the url significantly slows down the program, and on rare occasion does not work at all.

```-o, --output_file```: Provide the path for the output file. This program outputs an html, so remember that when creating a file name. 

```amniote_mass.py```: This program runs on all three classes of Amniotes. However, due to the large amount of missing data of body length for Aves and Reptilia, this program only generates summaries of body mass variables. This program has **three flags**:

```-d, --data_file```: same as above

```-o, --output_file```: same as above

```-c, --taxon_class```: This takes the taxon class you are interested in. Input ```'Aves'```, ```'Mammalia```, or ```Reptilia```. 

## What They Do:

####Both `Mammalia.py` and `amniote_mass.py`:####

After inputing your file, the program generates 5 figures and two tables:

**Figure 1**: This shows the natural log of body mass for every order. Box plots show the first quartile, and the whiskers show the 3rd quartile. Outliers are seen in red dots.

**Table 1**: Shows the mean mass in grams for every order in the class that you selected. This table **is interactive** and can be sorted by clicking on the mass header or order header. 

**Figure 2**: Shows the disparity of body mass for each order. This is created by calculating ln(max mass for each order) - ln(min mass for each order) and displaing those values. Log values are taken to normalize the data and put them in a reasonable scale. For example, the difference in mass of two whale species is a large number, while the difference between two mice is not. Scaled we find very different results. Take a look!

**Figure 3**: This shows the natural log of body mass for every family. Box plots show the first quartile, and the whiskers show the 3rd quartile. Outliers are seen in red dots.

**Table 2**: Shows the mean mass in grams for every family. This table **is interactive** and can be sorted by clicking on the mass header or order header. This is interactive and works just like **table 1**

**Figure 4**: Shows the disparity of body mass for each family. This works the same way as **figure 2** but at the family level.

**Figure 5**: Shows the 20 families with the largest mass difference (log scale) between the smallest and the largest. Again, perhaps not what is expected!

####Only `Mammalia.py`:####

The missing data from Aves and Reptilia makes them unsuitable for this portion of teh analyses, which investigates body length in the smae manner as above.

**Figure 6**: This shows the natural log of body length for every mammalian order. Box plots show the first quartile, and the whiskers show the 3rd quartile. Outliers are seen in red dots.

**Table 3**: Shows the mean length (cm) for every order in mammals. This table **is interactive** and can be sorted by clicking on the mass header or order header. 

**Figure 7**: Shows the disparity of body legnth for each mammalian order. This is created by calculating the difference in the same way as figure 2. Again, there may be some suprises!

**Figure 8**: This shows the natural log of body lenght for every family. Box plots show the first quartile, and the whiskers show the 3rd quartile. Outliers are seen in red dots.

**Table 4**: Shows the mean length in cm for every family. This table is interactive like the others.

**Figure 9**: Shows the disparity of length for each family. This works the same way as **figure 7** but at the family level.

**Figure 10**: Shows the 20 families with the largest difference in length (log scale) between the smallest and the largest.
