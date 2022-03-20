import sys

from domain import Graph
from repo import Repository
from service import Service
from ui import Ui
from tests import Test



test = Test()
#test.test_all()

graph = Graph(0, 0)
repo = Repository(graph)
service = Service(repo)
ui = Ui(service)


ui.start()

