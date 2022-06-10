from pathlib import Path
import subprocess
import time

SOURCE_PATH = '/'
FFMPEG_PATH = 'ffmpeg.exe'
ARGUMENT_PRE_IMAGE = '-r --directio=true mkv iso:'
ARGUMENT_PRE_FOLDER = '-r --directio=true mkv file:'
ARGUMENT_POST = 'all'
STORAGE_LOCATION = '/'


def wave2Mp3(inputs):
    # ffmpeg -i input-file.wav -vn -ar 44100 -ac 2 -b:a 192k output-file.mp3
    print("data: ", inputs)
    if inputs and inputs[1]:
        sourcePath = inputs[1]
    else:
        sourcePath = SOURCE_PATH
    listOfFiles = getListOfFiles(sourcePath)
    if len(listOfFiles) > 0:
        # print("now processing.....")
        # print(listOfFiles)
        executeWaveToMp3(listOfFiles)
    else:
        print("No files found in the folder: ", sourcePath)
    return 0


def getListOfFiles(sourcePath):
    types = '*.wav'  # the tuple of file types
    files_grabbed = []
    # for eachType in types:
        # path_pattern = os.path.join(sourcePath, type)
        # pths = glob.glob(path_pattern)
        #
        # match = re.compile(fnmatch.translate(type)).match
        # valid_pths = [pth for pth in pths if match(pth)]
        # files_grabbed.extend(valid_pths)

    topPath = Path(sourcePath).rglob(types)
    # print('topPath: ', topPath);
    files = [x for x in topPath]
    files_grabbed.extend(files)

    return files_grabbed


def executeWaveToMp3(files):
    isMPEG2Encoded = True
    for name in files:
        wavFullPath = name.__str__()
        fileName = wavFullPath.rsplit('\\', 1)[-1]
        mp3FullPath = wavFullPath.replace('.wav', '.mp3')
        # print("wav path: ", wavFullPath)
        # print("mp3 path: ", mp3FullPath)
        convertWav2Mp3(wavFullPath, mp3FullPath)


def convertWav2Mp3(wavFile, mp3File):
    # ffmpeg -i input-file.wav -vn -ar 44100 -ac 2 -b:a 192k output-file.mp3
        mp3EncodeCommand = 'ffmpeg.exe -i "' + wavFile + '" -vn -ar 44100 -ac 2 -b:a 256k "' + mp3File + '"'
        # print('command to execute: ', mp3EncodeCommand)
        executeExternalCommand(mp3EncodeCommand, "noOutput")
        deleteWavCommand = 'del /S /Q "' + wavFile + '"'
        # print('delete command to execute: ', deleteWavCommand)
        executeExternalCommand(deleteWavCommand, "noOutput")


def executeExternalCommand(execCmd, options=""):
    # print("executing: ", execCmd)
    if len(options) > 0:
        executeCmd = subprocess.Popen(execCmd, shell=True)
        executeCmd.wait()
    else:
        executeCmd = subprocess.Popen(execCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        executeCmd.wait()
    time.sleep(1)


def logs(message):
    print(message)
