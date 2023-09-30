# Interactive dashboard for signal comparison

An interactive dashboard to compare signal curves collected from a four channels sensor.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [License](#license)

## Project Overview

Create an interactive dashboard to comapre plots of a four channel sensor output. Separately plots all channels curve's and allows to select one curve for channels to make a direct comparison on a dedicated interactive plot.

I developed the code to plot and compare measurements during the optimization phase of TMek a rapid diagnostic test for malaria developed at Politecnico di Milano ([project scietific paper](https://ieeexplore.ieee.org/abstract/document/9924602)). 

## Features

- automatically and recursively plot .mat files starting from a root direcotry
- create interactive dashboard to look at single channels results and compares different channels results interactively

## Getting Started

The dashboard run on a local server created using Dash, accessible using any browser. Once lunched the __main__.py file, you simply need to open the link generated on the local host.

- Python code lunching the web server:
     ```webapp.run_server(port=os.getenv("PORT", "9999"))```

- Example of the output url to open:
    *Running on http://127.0.0.1:9999*

### Prerequisites

The code was written using the folowing packages version. Some features may not work on different versions.

At present the code only run with .mat extention files having the same structure of those reported in folder \data\example_measures.

*package name list and versions*

- dash             2.13.0
- numpy            1.22.3
- plotly           5.13.0
- pandas           1.4.2
- scipy            1.8.0

### Installation

To use the code simply clone the repo and lunch the __main__.py file

# License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.