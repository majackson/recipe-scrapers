from defaults import *
import subprocess

LOG_PATH = '/tmp/allergy_assistant'

subprocess.Popen(('mkdir -p %s' % LOG_PATH).split()).wait()
