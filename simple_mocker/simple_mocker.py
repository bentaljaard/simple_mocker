__version__ ='0.1'

import argparse
import os
import re
import yaml
from pprint import pprint


import tornado.web
from mock_handler import MockHandler


def setUp(self):
    super(BaseClass,self).setUp()
    with open(filename) as data_file:
        self.test_data = yaml.load(data_file)
    print(filename)
   

def get_app(mocks):
    #Create a generic route handler
    application = tornado.web.Application([
    (r"/.*", MockHandler, {"mocks":mocks}), ])
    application.listen(port)

    return application

def get_yaml_files(path):
    files = os.listdir(os.path.abspath(path))
    return filter(lambda file: re.match(".*\.yaml$", file), files)

def load_mocks(folder):
    # get list of files to load
    files = get_yaml_files(folder)
    mocks = {"mocks":[]}
    for file in files:
        with open(folder + "/" + file) as data_file:
            mock_file = yaml.load(data_file)
        print("Loaded " + file)
        mocks["mocks"] = mocks["mocks"] + mock_file["mocks"]
    return mocks


if __name__ == '__main__':
    # load commandline argumengts
    parser = argparse.ArgumentParser(prog='simple_mocker.py',description="Simple mocker allows you to define simple mocks")
    parser.add_argument('--port', '-p', help='Specify the listening port for your mock server', default=8888)
    parser.add_argument('--folder', '-f', help='Specify the folder that will be containing the mock definitions', default="../mock_definitions")
    parser.add_argument('--version', action='version', version='%(prog)s '+ __version__, help='Print the API Tester version')
    args = parser.parse_args()

    # port to start listener
    port = args.port

    # folder to load mocks from
    folder = args.folder

    mocks = load_mocks(folder)
    get_app(mocks)
    tornado.ioloop.IOLoop.current().start()


