[![GitHub version](https://badge.fury.io/gh/hgromer%2Fditto.svg)](https://badge.fury.io/gh/hgromer%2Fditto)
[![PyPI version](https://badge.fury.io/py/ditto-lib.svg)](https://badge.fury.io/py/ditto-lib)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Ditto: A data analysis library

**Ditto** is a data analysis library meant to make processing and accumulating data easier. It provides an easy to use API that is intuitive and allows the user to be more productive. **Ditto** utilizes different **Collections** to store data. These **Collections** are made of **Items**, and each **Item** is represented by various different **Attributes**. These **Collections** can be generated manually, or imported from various sources, such as csv files. An **Item** array that stores values called **Attributes**. Accessing, and modifying **Items** within these **Collections** is very user friendly.  

# Basic Usage

Assume we have the following csv file 'people.csv':

| Name | Weight | Age | 
| :-: | :-: | :-: |
| Jim | 160 | 20 | 
| Sally | 130 | 21 |
| Bob | 120 | 10 |
| Bill | 200 | 45 |
| Jen | 150 | 23 |

Below is an example of how to import the csv file into an **ItemCollection**:

```python

# Create the Item Collection by giving it a name
item_collection = ItemCollection('People')
# Import the csv file, giving a start_row and start_column to start at
item_collection.from_csv('people.csv', start_row=1, start_column=1)
```

The **from_csv** method assumes that the names of the items belonging to this **Collection** are located at column 0, and start at row **start_row**. All the columns from **start_column**, and onward are the attributes that will then be associated with the **Item** in that row. You can also use a string name to give the starting column, as shown below:

```python
item_collection.from_csv('people.csv', start_row=1, start_column='Weight')
```

Now that we are correctly storing our items within the **Collection**, we can access individual **Items** by name. We can also access each **Item's attributes** by name as well once the **Item** has been retrieved. Below is an example of how to retrieve the **Item** 'Bill', print all of it's **Attributes** and print the **Attribute** 'Weight':

```python
# Get the item
attributes = item_collection.get_item('Bill')
print(attributes)
>>> [200, 45]
# Print the attribute Weight
print(item_collection.item_attribute('Bill', 'Weight'))
>>> 200
```

In order to mantain consitency, all **Items** that belong to the same **Collection** must share the same set of **Attributes**. Additionally, **Items** store **Attributes** in the same order for every **Item** in a **Collection**. **Items** can have None type values associated with the **Attribute**, but it important to mantain the integrity of the **Collection** in this manner. In order to do this, when modifying **Items**, it is important to do so through the **Collection** API. Below is an example of how to add an attribute to an item:

```python
people.set_item_attribute('Bob', 3.5, 'GPA')
```

The **set_item_attribute** method will assign that **Attribute** to the **Item** given if it exists, if not it will create the **Attribute**, assign it to the **Item**, and update the entire **Collection**. Now, the **ItemCollection** will resemble the following:

| Name | Weight  |  Age | GPA |
| :-----: | :-: | :-: | :-: |
| Jim | 160 | 20 | |
| Sally | 130 | 21 | |
| Bob | 120 | 10 | |
| Bill | 200 | 45 | 3.5 |
| Jen | 150 | 23 | |

There are also some utilities that we can use in order to make analyzing information easier. We can merge and intersect **Collections**, as well as strip them to remove any noisy **Attributes**. Noisy **Attributes** are ones that contain the same value for every **Item** in a **Collection**. Assume we have another csv file called 'people2.csv':

| Name | Weight  |  Age | GPA |
| :-----: | :-: | :-: | :-: |
| Jim | 160 | 20 | 3.5 |
| Sally | 130 | 21 | 3.5 |
| Bob | 120 | 10 | 3.5 |
| Jen | 150 | 23 | 3.5 |
| Ashley | 200 | 24 | 3.5 |

 Below is an example of how to merge two **Collections**

```python
# Assume we have two Item Collection objects item_collection, to_merge
merged_collection = people.merge(people2, 'Merged Collection')
```

As a result, the merged_collection will look like the following:

| Name | Weight  |  Age | GPA |
| :-----: | :-: | :-: | :-: |
| Jim | 160 | 20 | 3.5 |
| Sally | 130 | 21 | 3.5 |
| Bob | 120 | 10 | 3.5 |
| Bill | 200 | 45 | 3.5 |
| Jen | 150 | 23 | 3.5 |
| Ashley | 200 | 24 | 3.5 |

When merging **Collections**, if any **Items** are shared, they will combine their **Attributes**. Now let's remove any noise from the **Collection** by deleting any **Attributes** that share the same value for all **Items**

```python
merged_collection.strip()
```

Results in:

| Name | Weight  |  Age |
| :-----: | :-: | :-: |
| Jim | 160 | 20 |
| Sally | 130 | 21 |
| Bob | 120 | 10 |
| Bill | 200 | 45 |
| Jen | 150 | 23 |
| Ashley | 200 | 24 |

Instead of merging, you can also intersect **Collections**, which will create a new **Collection** that contains only **Items** that are found in both **Collections**. Again, any discrepancies between **Item Attributes** will be resolved by merging same item attributes. An example of an intersection is shown below:

```python
# Assume we have two Item Collection object item_collection, to_intersect
intersected_collection = people.intersect(people2, 'Intersected Collection')
```

As a result the intersected_collection will look like the following:

| Name | Weight  |  Age | GPA |
| :-----: | :-: | :-: | :-: |
| Jim | 160 | 20 | 3.5 |
| Sally | 130 | 21 | 3.5 |
| Bob | 120 | 10 | 3.5 |
| Jen | 150 | 23 | 3.5 |

# Clustering Usage
**Ditto** provides a clustering framework that can be used to easily cluster data that has been imported by the library. The **ClusterCollection** is a class that makes this possible. When creating a **ClusterCollection**, you can pass it an amount of clusters to generate. For algorithms such as k-means clustering, cluster amounts must be manually specified. This will be overriden if a non cluster amount algorithm is run, such as mean shift or DBSCAN. Because the **ClusterCollection** derives from **ItemCollection**, they share functionality. 

Assume we have the following csv file called 'people.csv':

| Name | Weight  |  Age | GPA |
| :-----: | :-: | :-: | :-: |
| Jim | 160 | 20 | 3.5 |
| Sally | 130 | 21 | 3.5 |
| Bob | 120 | 10 | 3.5 |
| Bill | 200 | 45 | 3.5 |
| Jen | 150 | 23 | 3.5 |
| Ashley | 200 | 24 | 3.5 |

Below is an example of how to run the various clutering algorithms that are supported given a csv file 'file.csv':

```python
# Lets create our ClusterCollection and import a csv file
collection = ClusterCollection('Clustering Tutorial', cluster_amount=2)
collection.from_csv('people.csv')

# K-Means clustering
collection.run_kmean()

# Mean Shift clustering
collection.run_meanshift()

# DBSCAN clustering
collection.run_dbscan()
```

It is also possible to exclude **Attributes** when running clustering algorithms. Each clustering method takes a set of excluded attributes. This is an empty set by default, but can be included as shown below:

```python
collection.run_kmean(
    excluded_attributes={
        'Gender'
    }
)
```

Now that we've put our **ClusterCollection** through clustering algorithms, we can access individual **Clusters** to see which items have been placed where. Below is an example of how to access those clusters:

```python
# Print the names of all clusters
for cluster in collection.clusters:
    print(cluster.name)
>>> Cluster 0
>>> Cluster 1

# Print all items in each cluster
for cluster in collection.clusters:
    print("Cluster {}".format(cluster.name))
    for name, values in cluster.items.items():
        print("Item name {}, Item Values {}".format(name, values))
    print('-----------------------')

    >>> Item name Jim, Item Values ['160', '20', '0']
    >>> Item name Sally, Item Values ['130', '21', '1']
    >>> Item name Bob, Item Values ['120', '10', '0']
    >>> Item name Jen, Item Values ['150', '23', '1']
    >>> '-----------------------'
    >>> Cluster Cluster 1
    >>> Item name Billy, Item Values ['200', '45', '0']
    >>> Item name Ashley, Item Values ['200', '24', '1']
    >>> '-----------------------'
```

If we'd like to save these **Clusters** out to a file, we can do so by first converting them to **ItemCollections** and calling the to_csv method. Below is an example of how to store every cluster in collection to a file named after the cluster name:

```python
for cluster in collection.clusters:
    collection.cluster_as_itemcollection(cluster.name).to_csv(cluster.name)
```

You can also directly convert the **Cluster** to an **ItemCollection** by passing it the attributes it will store as shown below:

```python
for cluster in collection.clusters:
    cluster.as_itemcollection(collection.attributes).to_csv(cluster.name)
```

# Excel Workbook Usage

If we need to pull/store data in multi sheet excel WorkBooks, we can use the **Ditto Book** api to achieve these goals. An excel file is split into sheets, which are then stored as ItemCollections. Below we can load a Book directly from an excel file by passing the excel file name as well as a list of tuples which hold (start_row, start_column) values for each sheet that is being imported:

```python
book = Book('Book Name')
book.load('excel.xlsx', [(1,1), (1,1)])
```

We have loaded our Book. While loading from an excel file is useful, we can also load csv files into ItemCollections, and then store those collections as Book sheets. This method is far quicker than directly loading from an excel file:

```python
collection = ItemCollection('Collection Name')
collection.from_csv('file.csv')
book.add_sheet(collection)
```

Now lets look at all the sheets we have stored, then lets access one of the sheets and save it as it's own csv file:

```python
print(book.sheetnames)
>>> ["Sheet1", "Sheet2", "Collection Name"]
book.collection('Sheet1').to_csv('outfile.csv')
```

Now lets save the entire Book to an excel file

```python
book.save('outfile.xlsx')
```

Below you can find more methods and applications of the Ditto Book.


# Attribute Usage
The **Attribute** is a class that contains a name and boolean value is_descriptor. If an **Attribute** is defined as being a descriptor, then it will be used when running the **Item** it belongs to through certain algorithms, such as a clustering algorithm. This distinction was made for the User's convenience, and all **Attributes** will default to being a descriptor.

- **copy**: Returns a deep copy of the attribute

# Item Usage
The **Item** isn't a literal class in order to mantain performance efficiency. An **Item** is represented as an array of values. **Items** are tied **Collections** and should be accessed and modified through the **Collection's** API.

# ItemCollection Usage

The **ItemCollection** is the base class for all other **Collections** and have a variety of useful methods to help analyze and process data.

- **get_item**: Takes an item name. Returns the item if it is stored in the collection.
- **item_names**: Returns a list of all item names stored in the collection.
- **add_attribute**: Takes an attribute and adds it to the set of all attributes that pertain to the current collection, updates the collection's items accordingly.
- **remove_attribute**: Takes an attribute name and removes it from the set of all attributes that pertains to the current collection. Removes attributes from all items pertaining to the collection as well.
- **prune_attributes**: Takes a set to_keep, and boolean remove_ndescriptors. Remove all attributes who's names are not found in to_keep, defaults to an empty set. If you remove_ndescriptors is set to True, remove all non descirptors, defaults to False.
- **prune_preamble**: Takes a length. If the length is None, sets of the length of each preamble row to the amount of attributes. If not None sets the length of each preamble row to the legnth given. Defaults to None
- **contains_item**: Takes an item name. Returns True if that item is contained in the collection, False if not.
- **contains_attribute**: Takes an attribute name. Returns True if that attribute in contained in the collection. False if not.
- **set_item_attribute**: Takes an item name, an attribute value, attribute name, and is descriptor which defaults to True. If the item already has an attribute by that name, overrides it, if not, then adds it to the item. Updates the entire collection to ensure each item has the same set of attributes.
- **item_attribute**: Takes an item name, and an attribute name. Returns the attribute if it exists in the given item name.
- **attribute_index**: Takes an attribute name. Returns the index of the given attribute name. The index is the position of that attribute in every item's value array.
- **get_sorted**: Takes an attribute name, and a boolean value descending. Returns a list of tuples. The first item in the tuple will be the item name, the second item in the tuple will be the list of attributes pertaining to that item. If descending is False, returns in ascending order, else returns in descending order. Descending is set to False by default
- **merge**: Takes another collection, and name. Merges this collection with the collection given and assigns the new merged collection to the name given. If collections share the same items, but the items have different attributes, then item attributes will be merged.
- **copy**: Returns a deep copy of the collection.
- **wipe**: Reset this collection.
- **strip**: Accepts a threshold, a number between 1 and 0. If the percent of different values for a single attribute amongst all items is less than the threshold, remove it. Defaults to None, which will delete an attribute only if all items's share the same value for that attribute. Returns the name of the attributes that were stripped
- **from_csv**: Take a filename, an attribute start_row, an attribute start_column, a preamble_indexes, and a set of non descriptors. Imports the filename given to this collection, with attributes starting at the attribute start_row and attribute start_column given. If an attribute is imported that is also contained in the non descriptor set given, the attribute will be added as a non descriptor. The preamble_indexes is a tuple (starting row of preamble, end row of preamble). Assumes that the start_column containing the item names is at start_column 0. Attribute start_row defaults to 0, attribute start_column defaults to 1, preamble_indexes defaults to None, non_descriptors defaults to an empty set.
- **to_csv**: Takes a filename. Outputs the current collection to the given csv file.
- **random_forest_regressor**: Returns results in order of most important attributes to least important attributes. Results are returned in a list of tuples, where the first item in the tuple is the attribute name, and the second item is the importance of that attribute. More documenation can be found at https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html
- **detect_outliers**: Returns the list of items which are considered to be outliers. More information can be found at https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html
- **raw**: Accepts a set of attributes to exclude. Returns a pair. Returns a dict where 'values' contains the raw array data of all items, 'item_names' contains the list of all item names in order, and 'attribute_values' contains the list of attributes in order. Only the attributes that are considered descriptors will be added. Useful for using this library in conjuction with others such as numpy, scipy, etc. Abilities to exclude defaults to an empty set.
- **calc_rmse**: Takes a target score and an actual score. Both target score and actual score are attribute names. Returns the RMSE value of all items in the collection when comparing the value from their target score to their value in their actual score.
- **generate_error**: Takes a name, target score, and actual score. Both target score and actual score are attribute names. Takes the percent error of the value from the target score and actual score and generates a non descriptive attribute that will be stored at each item. The newly generated item's name will be the name passed.
- **calculate_similarity**: Take the name of two items, and a method. Returns their similarity score based on method's algorithm. Method will default to 'euc'.
- **calculate_all_similarities**: Takes an item name, and a method. Returns a list of tuples where the first value is the item the given item is being compared to, and the second value is the similarity score between to the two items. Will return similarity scores for all other items in the collection. Method will default to 'euc'.
- **descriptive_attributes**: Return a list of all the descriptive attributes stored in this collection. 
- **intersect**: Takes a collection. Returns a new collection that contains items located in both collections. Item attributes will be merged if the same item contains a set of different attributes.
- **rename**: Takes an item name, and a new item name. Renames the item to the new name. If an item with the new name is already being stored by the collection, the item will be overwritten.

# Cluster Usage

The **Cluster** is a class that stores items. It is utilized by the **ClusterCollection** and should rarely if ever be used in a raw fashion.

- **contains**: Take the name of an item and returns whether that item is stored in this cluster.
- **copy**: Returns a deep copy of the cluster object.
- **as_itemcollection**: Takes a boolean value copy. Returns an ItemCollection based on the cluster. Useful for if you want to export to a csv. If copy is set to True, will make a deep copy of the cluster. Copy is set to false by default.

# ClusterCollection Usage

The **ClusterCollection** is a child class of the **ItemCollection** class, and is utilized for clustering algorithms.

- **run_meanshift**: Accepts a set of attributes to exclude in the algorithm. Run meanshift algorithm. Clusters will be generated for you. Set defaults to the empty set.
- **run_kmean**: Accepts a set of attributes to exclude in the algorithm. Run kmean algorithm. Will create as many clusters as ClusterCollection contains cluster_amount. Set defaults to the empty set.
- **run_dbscan**: Accepts a set of attributes to exclude in the algorithm. Run dbscan algorithm. Clusters will be generated for you. Set defaults to the empty set.

# Book Usage

The **Book** is a module that can pull data from multi sheet excel WorkBooks into **ItemCollections**

- **load**: Takes a filename, starting indexes, and a set of non descriptors. The starting indexes are a list of tuples, where the first item in the tuple is the starting row for the current sheet, and the second item is the start column for the current sheet. The set of non_descriptors defaults to an empty set.
- **save**: Saves Book back to the file given.
- **value**: Takes a sheet name, an item name, and an attribute name. Returns the value at that given sheet cell. 
- **set_value**: Takes a sheet name, item name, value, attribute name, and is_descriptor. Sets the value of the cell at that sheet to the value given. Creates the attribute if it doesn't exist. non_descriptor defaults to False.
- **merge**: Takes a list of sheets stored by the Book to merge. Defaults to None, which merges all the sheets.
- **intersect**: Takes a list of sheets stored by the Book to intersect. Defaulst to None, which intersects all the sheets.
- **fill**: Takes a sheet name, item name, attribute name, color tuple, pattern type, and fill type. Fill the cell at the given sheet name with the given color and fill type. The color is a tuple, with the first item being the start color, and the second item being the end color. More information on excel styling can be found at the openpyxl website.
- **add_sheet**: Takes an ItemCollection. Adds that ItemCollection to the sheets included in the Book.
- **wipe**: Reset the Book
