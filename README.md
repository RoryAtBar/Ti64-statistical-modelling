# Ti64-statistical-modelling
## Authors: Rory Atlasi Barker & Guy Bowker
A database of material property data for Ti-6Al-4V alloy from existing literature and experiment.
The repo includes a python notebook tool for filtering and visualising stress-strain and beta volume fraction data for use in comparison against experimental and modelling data.
Titanium 6Al4V is presented here as an example, however any stress-strain data may be added by adding it's properties to the .yaml list and providing the data in .csv format in a directory whose path is included in the .yaml file.

### Instructions for contributors:
Thank you for choosing to contribute to this database of material properties - included here are some steps to help get started using this data in your own projects:

1. Firstly, you can either download this repository as a .zip file, or clone it to your chosen local directory address using the green button in the top right.

2. Navigate to the directory in a terminal on your computer. To add a paper/dataset begin by creating a new git branch of the repository using `git checkout -b <branchname>`. Remember to change `<yourbranchname>` to something useful such as the name of the database/paper with a timestamp.

3. Save the dataset as a .csv file in a discriptively named directory according to the type of data. Please follow examples already present in the repo.

3. Add the details of the paper/dataset as well as the relative file path to the relevant .yml file. (if you are adding a beta approach curve, add the dataset to beta-approach_curves.yml.)

4. Test your dataset has been added by running the corresponding example jupyter notebook.

Further attributes of the dataset which could be used to filter/sort data can be added but left blank with 'check' if this is unknown:
 - Strain rate
 - Temperature
 - Microstructure
 - Chemistry
 - Heating rate
 - Loading conditions
 - Texture