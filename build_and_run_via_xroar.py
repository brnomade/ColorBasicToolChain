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


def startXroarAsynchronously(the_arguments):
    presentScriptSection("STARTING COCO2B VIA XROAR")
    #
    try:
        os.chdir("C:\\CODING\\TRSCOLOR\\xroar-0.35.2-w64")
    except:
        print("")
        print("Aborting execution. Unable to switch to XROAR home folder.")
        sys.exit()
    #
    oscommand = safepath(os.path.join("C:\\CODING\\TRSCOLOR\\xroar-0.35.2-w64","xroar.exe"))
    oscommand = oscommand + " -run" 
    oscommand = oscommand + " " + safepath(the_arguments.file)
    #
    try:
        subprocess.Popen(oscommand)
    except:
        print("")
        print("Aborting execution. Unable to start XROAR.")
        sys.exit()
    #
    return oscommand


def presentScriptSection( sectionName ):
    # present a section
    print("")
    print("------------------------")
    print(sectionName.upper())
    print("------------------------")


def presentScriptTitle():
    # present the title
    print("------------------------")
    print("XROAR EXECUTER VERSION 0.1")
    print("DEVELOPED BY ANDRE BALLISTA")


def initialiseScriptArgumentsParser():
    # Initialise the arguments parser
    parser = argparse.ArgumentParser(description="Execute an input file in XROAR.")
    parser.add_argument("file",help="source file name to be executed. File extension is required. Filepath is not needed.")
    return parser


def presentScriptSettings(theArguments):
    # present the settings
    presentScriptSection("SETTINGS")
    print("SOURCE FILE:", theArguments.file)


presentScriptTitle()
inputArguments = initialiseScriptArgumentsParser().parse_args()
presentScriptSettings(inputArguments)
print(startXroarAsynchronously(inputArguments))


