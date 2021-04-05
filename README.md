# Delimag

Delimag is a tool to analyze Pandas DataFrame objects with multiselect records.
<br>

### Table of Contents

 1. [Installation](#installation)
 2. [Usage](#usage)
 3. [Project Motivation](#motivation)
 4. [Version](#version)
 5. [Licencing](#licencing)
 

<a id='installation'></a>
### Installation

**Dependencies:** <br>
There should be no necessary libraries to run the code here beyond the Anaconda distribution of Python. The code should run with no issues using Python versions 3.*.

* Python version 3.6.3 was used during the development of the project.
* The package is built on top of the Pandas library. Version 0.23.3 was used during development.
<br>

**User installation:** <br>
To be added


<a id='usage'></a>
### Usage
To be added.

<a id='motivation'></a>
### Project Motivation

For this project I was interrested in solving a problem I have ran accross many times during my work. <br>
I wanted to make it easier to analyse and aggregate data where one or more (Categorical) column includes multiple, delimited values.<br>
<br>

**The aim was to create a package that is able to apply the following on such delimited data:**
* Split the delimted values in a given column and return all distinct values.
* Apply a group by type aggregation, using the splitted distinct values of the categorical column as a groupper and an other numeric column on which the aggregation will be applied.
* Apply a cross-tabulation with two delimited categorical columns  as grouppers and one value column for the aggregation.
* Being able to use a wide range of aggregator functions.

**Beside solving the above problem, I also wanted to practice the following softwere engineering practices:**
* Creating an installable Package and uploading it to Pypi.
* Creating and using Unit Tests.
* Using Object Oriented Programming.
* Writing documentation (Including in-line comments, docstrings, and readme).
* Using Git and GitHub with multiple branches of develpment.

<a id='version'></a>
### Version
The current version of the project is v0.01.

<a id='licencing'></a>
### Licencing
The project is licenced under an MIT licence.<br>
Please see licencing details in the LICENSE.md file which you can find in the repository.
