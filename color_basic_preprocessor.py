import argparse
import configparser
import logging
import os
import subprocess
import datetime


# configuration file handling
glb_folder_root = os.getcwd()
glb_script_configuration_filename = os.path.join(glb_folder_root, os.path.basename(__file__).split(".")[0] + ".ini")
# log file handling
glb_msg_prefix_try = "Trying to"
glb_msg_prefix_fail = "Failed to"
glb_msg_prefix_ok = "Succeeded to"
glb_script_log_filename = os.path.join(glb_folder_root, os.path.basename(__file__).split(".")[0] + ".log")
logging.basicConfig(filename=glb_script_log_filename, level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s: %(process)d | %(thread)d | %(module)s | %(lineno)d |"
                           " %(funcName)s | %(message)s",
                    datefmt='%m/%d/%Y %I:%M:%S %p')


def present_script_section(a_section_name: str):
    print("")
    print("------------------------")
    print(a_section_name.upper())
    print("------------------------")


def present_script_title():
    print("CBPP - Color Basic Pre-Processor VERSION 0.1")
    print("Copyright(C) 2019 by Andre Ballista - www.oddpathsconsulting.co.uk")


def present_script_settings(a_configuration, the_arguments):
    # present the settings
    present_script_section("SETTINGS")
    print("input file:", the_arguments.input_file)
    print("output file:", the_arguments.output_file)
    print("bpp_phase:", the_arguments.bpp_phase)
    print("------------------------")


def initialise_script_arguments_parser():
    parser = argparse.ArgumentParser(description="Analyse and process an input file coded in ColorBasic and output a new version of the file with the pre-processing requirements resolved.")
    parser.add_argument("input_file", help="file name of the input file. file extension expected. a full file path can be provided with the file name")
    parser.add_argument("output_file", help="file name of the output file. file extension expected. a full file path can be provided with the file name")
    parser.add_argument("-bpp_phase", choices=['NO', 'YES'], default='YES', help="Executes BPP as step 0 to resolve includes and pragmas. Default value is YES.")
    return parser


def initialise_script_configuration_parser():
    # Initialise the configuration parser
    config = configparser.ConfigParser()
    config.read(glb_script_configuration_filename)
    return config


def remove_empty_lines(an_input_file_name, an_output_file_name):
    output_file_handler = open(an_output_file_name, "w")
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            if a_line.strip() != "":
                output_file_handler.write(a_line)
    output_file_handler.close()


def execute_bpp(an_input_file_name, an_output_file_name):
    my_time_log = datetime.datetime.utcnow()
    # initialise stuff
    my_status = False
    my_counter = 0
    retry_counter = 1
    current_dir = glb_folder_root
    # execute bpp
    os_command = "bpp.exe" + " " + an_input_file_name
    os_command = os_command + " " + an_output_file_name
    try:
        subprocess.run(os_command, shell=True)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        logging.error(message)
    else:
        my_status = True
    # report log
    log_msg = "Content %s - %s extract keyframes - default logic - pass %d - %d keyframes extracted"
    if my_status:
        logging.error(log_msg, "1", glb_msg_prefix_ok, retry_counter, my_counter)
    else:
        logging.error(log_msg, "1", glb_msg_prefix_fail, retry_counter, my_counter)


def add_line_numbers_to_output_file(an_input_file_name, an_output_file_name):
    line_number = 10
    line_increment = 5
    output_file_handler = open(an_output_file_name,"w")
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            output_file_handler.write(str(line_number) + " " + a_line)
            line_number = line_number + line_increment
    output_file_handler.close()


def prepare_goto_and_gosub_references(an_input_file_name, an_output_file_name):
    output_file_handler = open(an_output_file_name, "w")
    reference_dictionary = dict()
    line_number = 1
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            a_line_splitted = a_line.rstrip().split(" ")
            # print(a_line_splitted)
            a_line_number = a_line_splitted[0]
            a_reference_name = a_line_splitted[1][0:-1]
            a_prefix = a_line_splitted[1][0]
            a_terminator = a_line_splitted[1][-1]
            if a_prefix == "_":
                if a_terminator == ":":
                    if a_reference_name in reference_dictionary.keys():
                        print("syntax error - line", line_number, "Duplicated GOTO/GOSUB reference name found.", a_line)
                    reference_dictionary[a_reference_name] = a_line_number
                    output_file_handler.write(a_line_number + " " + "'" + a_reference_name + "\n")
                else:
                    print("syntax error - line", line_number, "missing terminator after destination reference name", a_line)
            else:
                output_file_handler.write(a_line)
            line_number = line_number + 1
    output_file_handler.close()
    # print(reference_dictionary)
    return reference_dictionary


def resolve_goto_references(an_input_file_name, an_output_file_name, a_reference_dictionary):
    # Scenarios:
    # scenario 01 -> VALID -> 10 SOME CODE:GOTO somewhere
    # scenario 02 -> VALID -> 10 SOME CODE: GOTO somewhere
    # scenario 03 -> VALID -> 10 GOTO somewhere
    # scenario 04 -> VALID -> 10 SOME CODE: GOTO_somewhere
    # scenario 05 -> VALID -> 10 SOME CODE:GOTO_somewhere
    # scenario 06 -> ERROR -> 10 GOTO [blank] missing the target
    # scenario 07 -> ERROR -> 10 GOTO undefined_somewhere
    # scenario 08 -> NO ACTION -> 10 ' whatever GOTO whatever
    # scenario 09 -> VALID -> 10 SOME CODE: GOTO _somewhere 'A COMMENT
    # scenario 10 -> INVALID -> 10 SOME CODE: GOTO somewhere: GOTO somewhere else
    output_file_handler = open(an_output_file_name, "w")
    line_number = 1
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            if "GOTO" in a_line:
                a_line_splitted = a_line.rpartition("GOTO")
                if "'" in a_line_splitted[0]:
                    # scenario 8
                    print("line", line_number, "- commented line - skipping.")
                elif a_line.count("GOTO") > 1:
                    # scenario 10
                    print("syntax error - line", line_number, "Multiple GOTO statements in a single line found.", a_line)
                elif a_line_splitted[2].strip() == "":
                    # scenario 6
                    print("syntax error - line", line_number, "GOTO reference missing.", a_line)
                else:
                    a_reference_name = a_line_splitted[2].strip().split(" ")[0]
                    if a_reference_name in a_reference_dictionary:
                        # scenarios 1, 2, 3, 4, 5 and 9.
                        a_line = a_line.replace(a_reference_name, str(a_reference_dictionary[a_reference_name]))
                    else:
                        # scenario 7
                        print("syntax error - line", line_number, "GOTO reference undefined.", a_line)
            output_file_handler.write(a_line)
            line_number = line_number + 1
    output_file_handler.close()


def resolve_gosub_references(an_input_file_name, an_output_file_name, a_reference_dictionary):
    # Scenarios:
    # scenario 01 -> VALID -> 10 SOME CODE:GOSUB somewhere
    # scenario 02 -> VALID -> 10 SOME CODE: GOSUB somewhere
    # scenario 03 -> VALID -> 10 GOSUB somewhere
    # scenario 04 -> VALID -> 10 SOME CODE: GOSUB_somewhere
    # scenario 05 -> VALID -> 10 SOME CODE:GOSUB_somewhere
    # scenario 06 -> ERROR -> 10 GOSUB [blank] missing the target
    # scenario 07 -> ERROR -> 10 GOSUB undefined_somewhere
    # scenario 08 -> NO ACTION -> 10 ' whatever GOSUB whatever
    # scenario 09 -> VALID -> 10 SOME CODE: GOSUB _somewhere 'A COMMENT
    # scenario 10 -> VALID -> 10 GOSUB here: GOSUB there: GOSUB futher:
    # scenario 11 -> VALID -> 10 GOSUB _somewhere:GOSUB_somewhere:GOSUB_somewhere"
    # scenario 12 -> VALID ->10 GOSUB _somewhere 'GOSUB _somewhere: GOSUB _somewhere"
    output_file_handler = open(an_output_file_name, "w")
    line_number = 1
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            if "GOSUB" in a_line:
                a_line_splitted = a_line.rpartition("GOSUB")
                if "'" in a_line_splitted[0]:
                    # scenario 8
                    print("line", line_number, "- commented line - skipping.")
                elif a_line.count("GOSUB") > 1:
                    # scenario 10, 11 and 12
                    for a_slice_of_line in a_line.split(":"):
                        a_split = a_slice_of_line.rpartition("GOSUB")
                        if a_split[1].strip() == "GOSUB":
                            a_reference_name = a_split[2].strip()
                            if a_reference_name == "":
                                # scenario 6
                                print("syntax error - line", line_number, "GOSUB reference missing.", a_line, "column", a_slice_of_line)
                            elif a_reference_name in a_reference_dictionary:
                                a_line = a_line.replace(a_reference_name, str(a_reference_dictionary[a_reference_name]))
                            else:
                                # scenario 7
                                print("syntax error - line", line_number, "GOSUB reference undefined.", a_line, "column", a_slice_of_line)
                elif a_line_splitted[2].strip() == "":
                    # scenario 6
                    print("syntax error - line", line_number, "GOSUB reference missing.", a_line)
                else:
                    a_reference_name = a_line_splitted[2].strip().split(" ")[0]
                    if a_reference_name in a_reference_dictionary:
                        # scenarios 1, 2, 3, 4, 5 and 9.
                        a_line = a_line.replace(a_reference_name, str(a_reference_dictionary[a_reference_name]))
                    else:
                        # scenario 7
                        print("syntax error - line", line_number, "GOSUB reference undefined.", a_line)
            output_file_handler.write(a_line)
            line_number = line_number + 1
    output_file_handler.close()


def final_pass(an_input_file_name, an_output_file_name):
    output_file_handler = open(an_output_file_name, "w")
    with open(an_input_file_name, "r") as input_file_handler:
        for a_line in input_file_handler:
            output_file_handler.write(a_line)
    output_file_handler.close()


# Script starts
present_script_title()
input_arguments = initialise_script_arguments_parser().parse_args()
configuration = initialise_script_configuration_parser()
present_script_settings(configuration, input_arguments)
logging.info("**** Color Basic Preprocessor started ")
#
source_filename_without_extension = input_arguments.input_file.split(".")[0]
# STEP 1 - run the BPP preprocessor
input_filename = input_arguments.input_file
output_filename = source_filename_without_extension + ".st1"
execute_bpp(input_filename, output_filename)
# STEP 2 - Remove empty lines from the source file
input_filename = output_filename
output_filename = source_filename_without_extension + ".st2"
remove_empty_lines(input_filename, output_filename)
# STEP 3 - add line numbers to file
input_filename = output_filename
output_filename = source_filename_without_extension + ".st3"
add_line_numbers_to_output_file(input_filename, output_filename)
# STEP 4 - prepare goto and gosub references
input_filename = output_filename
output_filename = source_filename_without_extension + ".st4"
a_dictionary = prepare_goto_and_gosub_references(input_filename, output_filename)
# STEP 5 - resolve goto references
input_filename = output_filename
output_filename = source_filename_without_extension + ".st5"
resolve_goto_references(input_filename, output_filename, a_dictionary)
# STEP 6 - resolve gosub references
input_filename = output_filename
output_filename = source_filename_without_extension + ".st6"
resolve_gosub_references(input_filename, output_filename, a_dictionary)
# step 7 - final pass
input_filename = output_filename
output_filename = input_arguments.output_file
final_pass(input_filename, output_filename)


