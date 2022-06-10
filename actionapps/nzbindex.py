import json
from datetime import datetime, time

import requests
from services import mysqldb

NZBINDEX_SERVER = ''
NZBINDEX_DOWNLOAD = ''
SAB_APIKEY = ""
SAB_SERVER = ""


def searchNzb(inputs):
    del inputs[0]
    if (len(inputs)) > 0:
        searchKey = ''.join(inputs)
        searchResult = getSearchResult(searchKey)
        processSearchResult(searchResult)
    else:
        # Get data from db
        searchKey = usingVtDb()
        for key in searchKey:
            searchResult = getSearchResult(key)
            processSearchResult(searchResult)


def processSearchResult(searchResult):
    if (len(searchResult['results'])) > 0:
        nzbConn = mysqldb.openDb()
        for result in searchResult['results']:
            # print('result: ', result)
            if result['size'] > 1500 and result['name'].find("GERMAN") == -1:
                # verify by time: result['posted'] => unix time
                nzb = "%s%s/%s" % (NZBINDEX_DOWNLOAD, result['id'], result['name'].replace(' ', '-'))
                if isDownloadedNzb(nzbConn, nzb) != True:
                    exportToSabnzbd(nzb)
        nzbConn.close()


def getSearchResult(searchTerm):
    # Search indexnzb.nl for 'searchTerm'
    response = requests.get(NZBINDEX_SERVER,
                            params={'q': searchTerm, 'max': 25,
                                    'sort': 'agedesc', 'minsize': 900, 'hidespam': 1, 'maxage': 3},
                            headers={'Accept': 'application/json'},
                            )
    data = json.loads(response.text)
    return data


def exportToSabnzbd(nzbUrl):
    print("nzbUrl away: ", nzbUrl)
    response = requests.get(SAB_SERVER,
                            params={'apikey': SAB_APIKEY, 'output': 'json',
                                    'mode': 'addurl', 'name': nzbUrl},
                            headers={"Content-Type": "application/xml", 'Accept': 'application/json; charset=utf-8'},
                            )


def usingVtDb():
    searchList = []
    sql = "Select description from mdt.todolist where subject = 'sabnzb' and deleted=0"
    nzbConn = mysqldb.openDb()
    nzbCursor = nzbConn.cursor()
    nzbCursor.execute(sql)
    # Fetch all the rows in a list of lists.
    results = nzbCursor.fetchall()
    for row in results:
        searchList.append(row[0])
    nzbConn.close()
    return searchList


def isDownloadedNzb(nzbConn, nzbUrl):
    isDownloaded = True
    if len(nzbUrl) > 300:
        nzbUrl = nzbUrl[0:299]

    sql = "Select id from mdt.dl_logs where app_dl = 'sabnzb' and ip_address= '%s'" % nzbUrl
    print('checking sql: ', sql)
    nzbCursor = nzbConn.cursor()
    nzbCursor.execute(sql)
    results = nzbCursor.fetchone()
    if not results:
        nzbConn.commit()
        dlTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO mdt.dl_logs (app_dl, ip_address,dl_time) VALUES ('sabnzb','%s','%s')" % (nzbUrl, dlTime)
        nzbCursor.execute(sql)
        isDownloaded = False
        nzbConn.commit()

    return isDownloaded;
