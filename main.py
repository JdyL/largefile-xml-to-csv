# HOW TO USE
# Open CMD, type in "Python [SCRIPTNAME] [INPUTFILENAME]"
# Output file will be in the same directory as the script
# Make sure Python 3 is installed for this to work

# Import libraries
import argparse
from xml.etree import ElementTree as ET
import os
import time

# Parser
parser = argparse.ArgumentParser(
    description='This script will extract elements from the input file (XML) into a CSV file,')
parser.add_argument('strings', type=str, nargs='+',
                    help='The input file for extraction')
args = parser.parse_args().strings

# File I/O
# Without any file extensions and path
inputFileName = (os.path.basename(os.path.splitext(args[0])[0]))
outputFileName = os.path.dirname(os.path.realpath(
    __file__)) + "\\" + inputFileName + "--output.csv"
outputFile = open(outputFileName, "w+")  # Output file

# Total lines written to file
totalLines = 0


def writeToFile(fileObj):  # This function writes to output file, parameter: string variable
    outputFile.write(fileObj.strip('\n') + splitCharacter)


start_time = time.time()


def fileSize(fileN):
    size = os.path.getsize(str(fileN))
    if size < 999:  # Less than a Kilobyte
        return str(size) + " Bytes"
    elif size < 999999:  # Less than a Megabyte
        return str(round(size/1000, 2)) + " KB(s)"
    elif size < 999999999:  # Less than a Gigabyte
        return str(round(size/1000000, 2)) + " MB(s)"
    elif size < 999999999999:  # Less than a Terabyte
        return str(round(size/1000000000, 2)) + " GB(s)"
    else:
        return str(size)

def clearArray(inputArray):
    outputArray = []
    for x in inputArray:
        outputArray.append("")

    return outputArray;

splitCharacter = ","  # Character splitting per field


fieldNames = ["TesterTag","EmptyTag","AnotherTag"]

outnames = list(fieldNames)
outnames[0] = '"TesterTag","EmptyTag","AnotherTag"'
outputFile.write(','.join(outnames))
outputFile.write("\n")

found = [""] * len(fieldNames)


# Main Procedure-------------------------------------------------------------------
for inputFiles in args:
    print("Input filesize: " + fileSize(inputFiles))
    print("\nReading file..." + str(inputFiles))
    e = ET.iterparse(inputFiles, events=("start", "end"))
    print("File read")
    print("---------------------")

    # Main (Procedural for now) Class

    lineAmount = 0

    print("Starting operation..\n")
    path = []  # Array of Element Tags
    info = []  # Array of Element Text

    print("Working on it..")

    idFound = False
    # Read per line
    for event, elem in e:
        delArray = 9000
        if event == 'start':
            # Add tag to Path array
            path.append(str(elem.tag).strip("\n").lstrip().rstrip())

        elif event == 'end':
            infoString = (str(elem.text).strip("\n")).lstrip().rstrip()
            info.append(infoString)  # Add text to info array
            for index, field in enumerate(fieldNames):

                if elem.tag == field:
                    found[index] = infoString
                    # idFound = True

            

            for x in found:
                writeToFile('"'+x+'"')
                outputFile.write("\n")
                found = clearArray(found)

            if len(info) and len(path) > 10000: # Clear memory every 10000 rows outputted
                del info[:delArray]
                del path[:delArray]

            elem.clear()  # Clear
    print("\n" + "Finished processing: " + inputFiles +
          " | Line in file: " + str(lineAmount) + "\n")
print("--------------------")
elapsed_time = time.time() - start_time
print("This took: " + str(round(elapsed_time)) + " seconds")
print("OUTPUT file: " + str(outputFileName))
print("Operation Completed. [" + str(totalLines) +
      "] lines/rows created in total\n")
print("--------------------")
