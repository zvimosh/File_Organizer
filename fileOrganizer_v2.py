# FileOrganizer
# Imports
import csv
import filecmp
import logging
import os
import shutil
import time

"""
This script organizes files into separate source folders,
the folder names are created from the file names.
The script will search all files within the 'Source Folder' recursively for any files with matching extensions
to the 'SourceFiles' list.
"""
""""
This script requires python version 3.6 or above.

To use the script, the user needs to set the following global variables:
    * 'sourceFolder' - the folder the script will list the files from.
    * 'sourceFiles' - the list of extensions the script will search for,
        you can add more extensions by adding according to the following example.
        '.ext' seperated by comma.
    * 'destFolder' - the destination folder that the script will move the files to, if the 'destFolder' is empty,
        the script will create the new files under the sourceFolder.
    * 'log_location' - the folder that the script log will be saved in, if 'log_location' is empty,
        the script will save the log in the 'destFolder'
    * enable_log = If 'True' the script will write logs, if false the script will not write ANY log. default is 'True'
    * enable_file_log = If 'True' the script will logs to a log file, if false the script will not write the log file.
      default is 'True'
    * enable_console_log = If 'True' the script will logs to console output, if false the script will not write the log.
      default is 'True'
    * generate_csv -If 'True' the script create a csv report of any file change in the following format:
    'Source Folder', 'Source File', 'Destination Folder', 'Destination File'
    * csv_report_name - sets the csv report name.
"""

# ----------------------------------------------------------------------------------------------------------------
# Global Variables
# ----------------------------------------------------------------------------------------------------------------
RUNS = 1
# Source folder where to look for files
sourceFolder = 'C:\\ScriptTest'

# list of extensions the script will handle
sourceFiles = ('.avi', '.mpg', '.mkv')

# destination folder where the new file folders will be created, empty will revert to source folder
destFolder = 'C:\\ScriptDest'

# if you want the folders to be created under the source folder
# destFolder = "C:\\ScriptTest\\Newfolder"

# destination folder where to store log and csv files - csv is optional
log_location = 'C:\\Scripts'

# if you want the script to check subfolders as well as the sourcefolders set this to true
recursive = True

# enables log
enable_log = True
enable_file_log = True
enable_console_log = True
# set it to true if you want to generate a csv report of the files, csv file will be saved in the log location
generate_csv = True
csv_report_name = "fileOrganizer_report.csv"

# create logger
logger = logging.getLogger('fileOrganizer')
logger.setLevel(logging.DEBUG)       # sets file logging level, set this as desired, accepts: debug, error, info

# ----------------------------------------------------------------------------------------------------------------
# DO NOT MODIFY THE SCRIPT BEYOND THIS POINT
# ----------------------------------------------------------------------------------------------------------------


# logger function
# creates logger handler
def configlogger():

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create file handler and set level to debug
    fh = logging.FileHandler(filename=os.path.join(log_location, 'fileOrganizer.log'), encoding='utf-8')
    fh.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')

    # add formatter to ch and fh
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch and fh to logger
    if enable_console_log:
        logger.addHandler(ch)
    if enable_file_log:
        logger.addHandler(fh)


# function dirscanner
# input: source Folder to scan, source File extensions to search
# returns 2 object lists: sub folder list and files list
def dirscanner(sourceFolder, sourceFiles):
    logger.debug('dirscanner - initiating [subfolders] and [files] lists')
    subfolders, files = [], []                                                # init lists of subfolders and files
    for entry in os.scandir(sourceFolder):                                    # itirate the first folder
        if os.path.isdir(entry):                                              # check if entry is folder
            subfolders.append(entry)                                          # add entry to subfolders list
            logger.debug('found sub folder: %s in folder [%s]', entry.name, os.path.dirname(entry))
        if os.path.isfile(entry):                                             # check if enrty is file
            if os.path.splitext(entry.name)[1] in sourceFiles:                # check if entry has the right extensions
                files.append(entry)                                           # add entry to files list
                logger.info('found file: [%s] in folder [%s]', entry.name, os.path.dirname(entry))
    if recursive:                                                             # check if to search recursively
        for sourceFolder in list(subfolders):                                 # recursive check in all subfolders
            r_subfolders, r_files = dirscanner(sourceFolder, sourceFiles)     # do recursion function
            subfolders.extend(r_subfolders)                                   # append subfolder to list
            files.extend(r_files)                                             # append subfile to list
    return subfolders, files                                                  # return subfolders and files lists


# function createfolder
# input: destination folder to move the files to, the list of files created by dirscanner function
# must run dirscanner first
# returns an object list of created folders
def createfolder(destfolder, list_files):
    createdfolder = []                                                        # init list of created folders
    for folder in list_files:                                                 # iterate through list of files
        file_name = os.path.splitext(folder.name)                             # save file name without extension
        destfolder_name = (os.path.join(destfolder, file_name[0]))            # save destination folder name
        logger.debug('folder: [%s] created', destfolder_name)
        try:
            os.mkdir(destfolder_name)                                         # create destination folder
        except FileExistsError:                                               # handle folder exists error
            logger.warning('[%s] folder already exists', destfolder_name)
            pass
        except Exception as err:                                              # log other errors
            logger.warning('error returned: ([%s]) ', err)
            raise
        createdfolder.append(destfolder_name)                                 # add created folder object to list
    return createdfolder                                                      # return a list of creted folders


def movefiles(destfolder_name, list_files):
    for file in list_files:
        destfolderfull = os.path.join(destfolder_name, os.path.splitext(file.name)[0])
        destfilefull = os.path.join(destfolderfull, file.name)
        if os.path.exists(destfilefull):
            if comparefile(file.path, destfilefull):
                try:
                    shutil.move(file.path, os.path.join(destfolderfull, file.name))
                    logger.warning('[%s] already exists in folder [%s], and its contents is matching the source file, '
                                   'file will be replaced', file.name, destfolderfull)
                    if generate_csv:
                        f = open(os.path.join(log_location, csv_report_name), "a")
                        print(file.path + "," + file.name + "," + destfolderfull + "," + file.name, file=f)
                        f.close()
                except OSError as err:
                    logger.error('[%s]', err)
                    raise
            else:
                filenewname = os.path.splitext(file.name)[0] + '_copy' + os.path.splitext(file.name)[1]
                try:
                    shutil.move(file.path, os.path.join(destfolderfull, filenewname))
                    logger.warning('[%s] already exists in folder [%s], and its contents does not match the '
                                   'source file, ''file will be created as a copy', file.name, destfolderfull)
                    if generate_csv:
                        f = open(os.path.join(log_location, csv_report_name), "a")
                        print(file.path + "," + file.name + "," + destfolderfull + "," + filenewname, file=f)
                        f.close()
                except OSError as err:
                    logger.error('[%s]', err)
                    raise
        else:
            try:
                shutil.move(file.path, os.path.join(destfolderfull, file.name))
                logger.info('[%s] did not exist in folder [%s], moving file', file.name, destfolderfull)
                if generate_csv:
                    f = open(os.path.join(log_location, csv_report_name), "a")
                    print(file.path + "," + file.name + "," + destfolderfull + "," + file.name, file=f)
                    f.close()
            except OSError as err:
                logger.error('[%s]', err)
                raise


def deleteemptyfolders(subfolders_list):
    for folder in subfolders_list:
        if not os.listdir(folder):
            logger.info('[%s] is empty, will delete it', folder.path)
            try:
                os.rmdir(folder)
            except OSError as err:
                logger.error('[%s]', err)


def comparefile(file, destfilefull):
    return filecmp.cmp(file, destfilefull)


if __name__ == '__main__':
    if enable_log:
        configlogger()
    logger.info('-------------------------------------------------------------------------------------------------')
    logger.info('START OF SCRIPT')
    logger.info('-------------------------------------------------------------------------------------------------\n')

    # Sanity checks
    logger.debug('CHECK - checking if sourceFolder is set')
    if sourceFolder == '':
        logger.error('CHECK - Source Folder must be configured for the script to run, exists script')
        exit(1)
    else:
        logger.debug('CHECK - sourceFolder is set to: [%s]', sourceFolder)
    logger.debug('CHECK - checking if destFolder is set')
    if destFolder == '':
        logger.warning('CHECK - Destination Folder was not configured, using source folder')
        destFolder = sourceFolder
    else:
        logger.debug('CHECK - destFolder is set to: [%s]', destFolder)
    logger.debug('CHECK - checking if log_location is set')
    if log_location == '':
        logger.warning('Log location Folder was not configured, using destination folder')
        log_location = destFolder
    else:
        logger.debug('CHECK - log_location is set to: [%s]', log_location)
    logger.debug('CHECK - checking if generate_csv is set')
    if generate_csv:
        try:
            f = open(os.path.join(log_location, csv_report_name), "w")
            logger.debug('CHECK - generate_csv is set to: [%s]', os.path.join(log_location, csv_report_name))
        except OSError as e:
            logger.error('CHECK - [%s]', e, "setting generate_csv to false")
            generate_csv = False
        if generate_csv:
            f = open(os.path.join(log_location, csv_report_name), "w")
            f.write("Source Folder, Source File, Destination Folder, Destination File")
            f.write("\n")
            f.close()
            logger.debug('CHECK - created csv file [%s]', os.path.join(log_location, csv_report_name))

    # start scan
    logger.debug('Time - Setting start time of actual script')
    start_time = time.time_ns()
    logger.debug('RUN - running script functions')
    for i in range(RUNS):
        logger.info('listing files found in source folder: [%s]', sourceFolder)
        list_subfolders, list_files = dirscanner(sourceFolder, sourceFiles)
        logger.info('creating folders in destination folder: [%s]', destFolder)
        createdfolder = createfolder(destFolder, list_files)
        logger.info('moving files from source folder to destination folder')
        movefiles(destFolder, list_files)
        logger.info('deleting empty folders in source folder')
        deleteemptyfolders(list_subfolders)
    logger.debug('Time - Setting end time of actual script')
    end_time = time.time_ns()
    logger.debug('Time - calculating run time')
    total_time = end_time - start_time
    logger.info(f'script ran for:[{total_time / 1000 / 1000 / RUNS:.0f}ms]')
    logger.info('-------------------------------------------------------------------------------------------------')
    logger.info('END OF SCRIPT')
    logger.info('-------------------------------------------------------------------------------------------------\n')

# print('created folder: ', createdfolder)
    # for i in createdfolder:
    #    print("created folder:", os.path.basename(i), 'in full path: ', i)
    # for file in list_files:
    #    movefiles(destFolder, file)

    # to get parent folder name from list_files use:  os.path.split(os.path.dirname(i.path))[1]
    # to get created folder name use: os.path.basename(i)