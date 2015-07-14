__author__ = 'besil'


url = "http://curia.europa.eu/juris/document/document_print.jsf?doclang=IT&pageIndex=0&part=1&mode=req&docid={}"
stopped_job = True

def crawl(min_size=5000, start_id=0):
    global stopped_job
    import time, urllib.request
    doc_id = start_id
    crawled_docs = 0

    while not stopped_job:

        f = urllib.request.urlopen(url.format(doc_id))
        outname = "data/document_{}.html".format(doc_id)
        data = f.read().decode("utf-8")

        # print("{} -> {}: {}".format(outname, len(data), len(data) > 4610))
        if len(data) > min_size:
            with open(outname, "w") as out:
                out.write(data)
                out.flush()

        time.sleep(1)
        doc_id += 1
        crawled_docs += 1
        if crawled_docs % 10 == 0: print("Crawled {} documents".format(crawled_docs))

    print("Stopped crawl")

def pre_check():
    import sys

    major_version = sys.version_info[0]
    if major_version != 3:
        raise Exception("You must use python3")
    try:
        import bottle
        import elasticsearch
    except ImportError:
        from subprocess import call

        call(["pip3", "install", "bottle"])

if __name__ == '__main__':
    # Per attivare il job: curl http://localhost:8150/start
    # Per stoppare il job: curl http://localhost:8150/stop

    pre_check()

    from bottle import run, get
    from threading import Thread

    @get("/start")
    def start_job():
        global stopped_job

        print("Starting job")
        stopped_job = False
        t = Thread(target=crawl, kwargs={"min_size": 4610, "start_id": 49331})
        t.start()
        print("Job started")
        return "Job started\r\n"

    @get("/stop")
    def stop_job():
        global stopped_job
        stopped_job = True
        print("Stopping job")
        return "Stopping job\r\n"

    run(host="localhost", port=8150, debug=True)
