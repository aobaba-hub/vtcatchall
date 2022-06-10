from pathlib import Path
import subprocess
import time

SOURCE_PATH = '/'
MAKEMKV_PATH = 'makemkvcon64.exe'
ARGUMENT_PRE_IMAGE = '-r --directio=true mkv iso:'
ARGUMENT_PRE_FOLDER = '-r --directio=true mkv file:'
ARGUMENT_POST = 'all'
STORAGE_LOCATION = ''
MKVMERGE = 'mkvmerge.exe'


def convert2mkv(inputs):
    print("data: ", inputs)
    if inputs and inputs[1]:
        sourcePath = inputs[1]
    else:
        sourcePath = SOURCE_PATH
    listOfFiles = getListOfFiles(sourcePath)
    if len(listOfFiles) > 0:
        # print("now processing.....")
        # print(listOfFiles)
        executeMakemkv(listOfFiles)
    else:
        print("No files found in the folder: ", sourcePath)
    return 0


def getListOfFiles(sourcePath):
    types = ('*.img', '*.iso', 'VIDEO_TS', 'BDMV')  # the tuple of file types
    files_grabbed = []
    for eachType in types:
        # path_pattern = os.path.join(sourcePath, type)
        # pths = glob.glob(path_pattern)
        #
        # match = re.compile(fnmatch.translate(type)).match
        # valid_pths = [pth for pth in pths if match(pth)]
        # files_grabbed.extend(valid_pths)

        topPath = Path(sourcePath).rglob(eachType)
        files = [x for x in topPath]
        files_grabbed.extend(files)

    return files_grabbed


def executeMakemkv(files):
    isMPEG2Encoded = True
    for name in files:
        isSuccessfulMkv = True
        isoFullPath = name.__str__()
        fileName = isoFullPath.rsplit('\\', 1)[-1]
        print("processing: ", isoFullPath)
        #       Check out if folder or image
        if isoFullPath.find("VIDEO_TS") == -1 and isoFullPath.find("BDMV") == -1:
            # image processing
            mkvCommand = MAKEMKV_PATH + " " + ARGUMENT_PRE_IMAGE + "\"" + isoFullPath + "\" " + ARGUMENT_POST + " " + STORAGE_LOCATION
            print("processing image: ", mkvCommand)
            fileName = fileName.rsplit('.', 1)[0]
        else:
            # folder processing
            # take take previous folder and make it the file name
            if isoFullPath.find("BDMV") >= 0:
                # This is bluray folder
                videoPath = isoFullPath.rsplit('\\', 1)[0]
                isMPEG2Encoded = False
            else:
                videoPath = isoFullPath
            fileName = isoFullPath.rsplit('\\', 2)[1]

            mkvCommand = MAKEMKV_PATH + " " + ARGUMENT_PRE_FOLDER + "\"" + videoPath + "\" " + ARGUMENT_POST + " " + STORAGE_LOCATION
            print("processing video: ", mkvCommand)

        print("fileName: ", fileName)
        p = subprocess.Popen(mkvCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            #             print(line)
            if line.__str__().find("Failed") != -1:
                print("ERROR processing file: ", isoFullPath)
                print("ERROR: ", line)
                isSuccessfulMkv = False
        p.wait()
        if isSuccessfulMkv:
            time.sleep(2)
            if isMPEG2Encoded:
                convertMkv2Mpeg4(fileName)
            else:
                renameMkvToUniqueName(fileName)
            cleanupLegacy(isoFullPath)


def convertMkv2Mpeg4(uniqueName):
    mkvName = uniqueName
    movieFiles = Path(STORAGE_LOCATION).rglob('title_t*.mkv')
    mkvFiles = [x for x in movieFiles]
    for mkvFile in mkvFiles:
        fileName = mkvFile.__str__()
        fileExtension = '_' + fileName.rsplit('_', 1)[-1]
        mpeg4EncodeCommand = 'ffmpeg.exe -i ' + fileName + ' "' + STORAGE_LOCATION + "\\" + mkvName + fileExtension + '"'
        executeExternalCommand(mpeg4EncodeCommand, "noOutput")
        deleteMpeg2FilesCommand = 'del /S /Q "' + fileName + '"'
        executeExternalCommand(deleteMpeg2FilesCommand)


def renameMkvToUniqueName(uniqueName):
    mkvName = uniqueName
    movieFiles = Path(STORAGE_LOCATION).rglob('title_t*.mkv')
    mkvFiles = [x for x in movieFiles]
    for mkvFile in mkvFiles:
        fileName = mkvFile.__str__()
        fileExtension = '_' + fileName.rsplit('_', 1)[-1]
        renameCommand = 'ren ' + fileName + ' "' + mkvName + fileExtension + '"'
        executeExternalCommand(renameCommand)


def cleanupLegacy(isoPath):
    #     print("cleanup processing: ", isoPath)
    pathToIsoFile = isoPath.rsplit('\\', 1)[0]
    # deleting existing iso
    deleteCommand = 'del /S /Q "' + isoPath + '"'
    # if folder is found, command to delete entire folder
    if isoPath.find("VIDEO_TS") != -1 or isoPath.find("BDMV") != -1:
        deleteCommand = 'rd /S /Q "' + isoPath + '"'

    executeExternalCommand(deleteCommand)
    # move all mkvs to current path
    moveCommand = 'move /Y "' + STORAGE_LOCATION + '\\*.mkv" "' + pathToIsoFile + '"'
    executeExternalCommand(moveCommand)


def executeExternalCommand(execCmd, options=""):
    print("executing: ", execCmd)
    if len(options) > 0:
        executeCmd = subprocess.Popen(execCmd, shell=True)
        executeCmd.wait()
    else:
        executeCmd = subprocess.Popen(execCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        executeCmd.wait()
    time.sleep(1)


def logs(message):
    print(message)
