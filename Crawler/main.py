__author__ = 'besil'

import urllib.request
import time

if __name__ == '__main__':
    url = "http://curia.europa.eu/juris/document/document_print.jsf?doclang=IT&pageIndex=0&part=1&mode=req&docid={}"

    docid = 49331
    limit = docid + 1000

    while (docid < limit):
        f = urllib.request.urlopen(url.format(docid))

        outname = "document_{}.html".format(docid)

        data = f.read().decode("utf-8")
        print("{} -> {}".format(outname, len(data)))
        if (len(data) > 4610):
            with open(outname, "w") as out:
                out.write(data)

        time.sleep(1)
        docid += 1

        print("Document: {}".format(docid))
