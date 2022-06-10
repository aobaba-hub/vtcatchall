import urllib.request
import sys
import os


def downloadFiles():
    print("Processing")
    inputFile = getInputFile()
    if inputFile:
        readInputFile(inputFile)
    else:
        print("Error - empty input file for link")


def sendGetFile(downloadUrl, archiveFolder):
    print("getting file..." + downloadUrl)
    chunks = downloadUrl.split('/')
    fileName = chunks[len(chunks) - 1]
    urllib.request.urlretrieve(downloadUrl, archiveFolder + '/' + fileName)
    print("save in : " + archiveFolder + '/' + fileName)


def readInputFile(fileOpen):
    # Creat folder with same name as file

    folderName = fileOpen.split('/').pop().split('.').pop(0)
    try:
        with open(fileOpen, 'r') as file:
            os.mkdir(folderName)
            contents = file.readlines()
            for i in range(len(contents)):
                urlToGet = contents[i].strip()
                sendGetFile(urlToGet, folderName)
    except IOError:
        print("File not found: ", fileOpen)


# END readInputFile

def getInputFile():
    # fileToOpen = "assets/HienNhanVietNam.1txt"
    fileInput = sys.argv.pop()
    # print("fileInput: ", fileInput)
    return fileInput
