# File_Organizer
# 
# This script organizes files into separate source folders,
# the folder names are created from the file names.
# The script will search all files within the 'Source Folder' recursively for any files with matching extensions
# to the 'SourceFiles' list.
# ---------------------------------------------------------------------------------------------------------------
# Author: Zvi Moshkovitz
# Email: z*******@gmail.com
# Date: 25/03/2021
# Version: 2
# ---------------------------------------------------------------------------------------------------------------
# 
# This script requires python version 3.6 or above.
# 
# To use the script, the user needs to set the following global variables:
#     * 'sourceFolder' - the folder the script will list the files from.
#     * 'sourceFiles' - the list of extensions the script will search for,
#         you can add more extensions by adding according to the following example.
#         '.ext' seperated by comma.
#     * 'destFolder' - the destination folder that the script will move the files to, if the 'destFolder' is empty,
#         the script will create the new files under the sourceFolder.
#    * 'log_location' - the folder that the script log will be saved in, if 'log_location' is empty,
#         the script will save the log in the 'destFolder'
#     * enable_log = If 'True' the script will write logs, if false the script will not write ANY log. default is 'True'
#     * enable_file_log = If 'True' the script will logs to a log file, if false the script will not write the log file.
#       default is 'True'
#     * enable_console_log = If 'True' the script will logs to console output, if false the script will not write the log.
#       default is 'True'
#     * generate_csv -If 'True' the script create a csv report of any file change in the following format:
#     'Source Folder', 'Source File', 'Destination Folder', 'Destination File'
#     * csv_report_name - sets the csv report name.
# 
