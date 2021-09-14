# Imports
import csv
import filecmp
import logging
import os
import shutil
import time
import confuse

config = confuse.Configuration('test')
config.set_file('./config.yaml')
Paths = config['Paths'].get()
source_folder = config['Paths']['source_folder'].get()
destination_folder = config['Paths']['destination_folder'].get()
print(Paths)
print(source_folder)
print(destination_folder)


