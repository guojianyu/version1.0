import os

father_path=os.path.abspath(os.path.dirname(__file__))
curdir = os.path.abspath(os.path.dirname(__file__))
script_path = os.path.join(curdir,'kind'+'.py')
print (script_path)