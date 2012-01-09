from defaults import *
import subprocess

LOG_PATH = '/tmp/recipe_scrapers'

subprocess.Popen(('mkdir -p %s' % LOG_PATH).split()).wait()
