__author__ = 'besil'

url_server_port = 8500
url_server_host = "localhost"


def check():
    import sys

    major_version = sys.version_info[0]
    if major_version != 3:
        raise Exception("You must use python3")

    modules = ["bottle", "elasticsearch"]
    from subprocess import call

    for module in modules:
        try:
            __import__(module)
        except ImportError:
            print("Installing module {}".format(module))
            call(["pip3", "install", module])
