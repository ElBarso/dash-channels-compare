import os
from dataVizLib import load_files, webapp_creator


if __name__ == '__main__':

    # extension and folder path of the files to plot
    file_extension = ".mat"
    input_path = r".\data\example_measures"

    # Load the files to plot and return plotly.Graph_Objects and a dictionary containing loaded file info
    # used to set up the plot layout
    measures, tagToColor_dictionary = load_files(input_path, file_extension)

    # Create the dash web app, fill it with contents to plot and set the page layout
    # The lunch the server
    webapp = webapp_creator(measures, tagToColor_dictionary)
    webapp.run_server(port=os.getenv("PORT", "9999"))