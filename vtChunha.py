import sys
from actionapps import nzbindex, convertMkv, whois, getFileUrl, passwordManager, wav2Mp3, mouseControl


def getInputArguments():
    del sys.argv[0]
    return sys.argv


def executeApp(arguments):
    app = arguments[0]
    print('arguments: ', arguments)
    print('app: ', app)
    return {
        'convert': convertMkv.convert2mkv,
        'wav2mp3': wav2Mp3.wave2Mp3,
        'whois': whois.whoisDomain,
        'nzb': nzbindex.searchNzb,
        'getfile': getFileUrl.downloadFiles,
        'passwd': passwordManager.managePassword,
        'mouse': mouseControl.moveMouse,
    }.get(app, helperManual)  # invalid request


def helperManual(userInput):
    print("help........", userInput)


args = getInputArguments()
print("args: ", args)
# Execute function
executeApp(args)(args)

sys.exit()
