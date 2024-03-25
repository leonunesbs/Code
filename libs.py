

import os

global root_directory, output_folder

root_directory = os.path.dirname(os.path.abspath(__file__))
output_folder = os.path.join(root_directory, 'output')
