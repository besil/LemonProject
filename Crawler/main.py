__author__ = 'besil'

import urllib.request
import time
from threading import Thread

from bottle import run, get

url = "http://curia.europa.eu/juris/document/document_print.jsf?doclang=IT&pageIndex=0&part=1&mode=req&docid={}"
stopped_job = True
current_id = 49331


def crawl():
    global stopped_job
    docid = current_id

    while not stopped_job:
        f = urllib.request.urlopen(url.format(docid))
        outname = "data/document_{}.html".format(docid)
        data = f.read().decode("utf-8")

        print("{} -> {}: {}".format(outname, len(data), len(data) > 4610))
        if (len(data) > 4610):
            print("Saving")
            with open(outname, "w") as out:
                out.write(data)
                out.flush()

        time.sleep(1)
        docid += 1

    print("Stopped crawl")


@get("/start")
def start_job():
    global stopped_job
    print("Starting job")
    stopped_job = False
    t = Thread(target=crawl)
    t.start()
    print("Job started")
    return "Job started\r\n"


@get("/stop")
def stop_job():
    global stopped_job
    stopped_job = True
    print("Stopping job")
    return "Stopping job\r\n"

if __name__ == '__main__':
    # Per attivare il job: curl curl http://localhost:8150/start
    # Per stoppare il job: curl http://localhost:8150/stop

    run(host="localhost", port=8150, debug=True)
