# Interactive dashboard for signal comparison

[An interactive dashboard to compare signal curves collected from a four channels sensor.]

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Project Overview

Create an interactive dashboard to comapre plots of a four channel sensor output. Separately plots all channels curve's and allows to select one curve for channels to make a direct comaprison on a dedicated interactive plot.

## Features

- automatically and recursively plot .mat files starting from a root direcotry
- create interactive dashboard to look at single channels results and compare different channels results interactively

## Getting Started

The dashboard run on a local server created using Dash, accessible using any browserOnce lunched the __main__.py file, you simply need to open the link generated on the local host.

Python code lunching thh web server:

webapp.run_server(port=os.getenv("PORT", "9999"))

Example of the output url to open:

Running on http://127.0.0.1:9999

To use this code you need .mat file input with the same structure of those reported in folder \data\example_measures.

### Prerequisites

The code was written using the folowing packages version. Some features may not work on different versions.

#### package-name     version

- dash             2.13.0
- numpy            1.22.3
- plotly           5.13.0
- pandas           1.4.2
- scipy            1.8.0

### Installation

To use the code simply clone the repo and lunch the __main__.py file

# License
[Specify the license under which your project is distributed. If you're unsure, you can use an open-source license like MIT or Apache 2.0.]

# Acknowledgments
[Give credit to any individuals, projects, or resources that you used or were inspired by while creating your project.]