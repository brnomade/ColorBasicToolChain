import sys
import os
import configparser
import argparse
import subprocess

def safepath( str ):
    # function to handle windows path names with empty spaces
    # in linux or ios this function is neutral
    if sys.platform.startswith('win'):
        stringcommand = '"' + str + '"'
    else:
        stringcommand = str
    return stringcommand


def copyFileToDsk(the_arguments):
    # Copy a aFileName to a aDskFileName 
    # imgtool put coco_jvc_rsdos test.dsk mtxt1v2.bas mtx4B.BAS --ftype=basic --filter=cocobas
    #
    print("Copying '" + the_arguments.file + "' to '" + the_arguments.dsk)
    oscommand = safepath( os.path.join("C:\\CODING\\TRSCOLOR\\mame0210_64bit", "imgtool.exe") )
    oscommand = oscommand + " put coco_jvc_rsdos"
    oscommand = oscommand + " " + safepath(the_arguments.dsk)
    oscommand = oscommand + " " + safepath(the_arguments.file)
    oscommand = oscommand + " " + the_arguments.name.capitalize()
    oscommand = oscommand + " --ftype=basic --filter=cocobas"
    print(oscommand)
    print(subprocess.run(oscommand, shell=True).returncode)


def presentScriptSection( sectionName ):
    # present a section
    print("")
    print("------------------------")
    print(sectionName.upper())
    print("------------------------")


def presentScriptTitle():
    # present the title
    print("------------------------")
    print("COPY TO DSK VERSION 0.1")
    print("DEVELOPED BY ANDRE BALLISTA")


def initialiseScriptArgumentsParser():
    # Initialise the arguments parser
    parser = argparse.ArgumentParser(description="Execute an input file in XROAR.")
    parser.add_argument("file",help="source file to be copied. File extension is required. Filepath is required.")
    parser.add_argument("dsk",help="DSK file where the source file will be placed. File extension is required. Filepath is required'.")
    parser.add_argument("name",help="name to be used for file when saving into the dsk file. File extension is required. Filepath is not needed'.")
    return parser


def presentScriptSettings(theArguments):
    # present the settings
    presentScriptSection("SETTINGS")
    print("SOURCE FILE:", theArguments.file)
    print("PROJECT DSK FILE:", theArguments.dsk)
    print("NAME TO BE USED FOR FILE:", theArguments.name)


presentScriptTitle()
inputArguments = initialiseScriptArgumentsParser().parse_args()
presentScriptSettings(inputArguments)
copyFileToDsk(inputArguments)

