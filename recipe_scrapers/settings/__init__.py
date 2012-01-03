import os

if os.environ.get('SCRAPERSCONTEXT') == 'production':
    from production import *
elif os.environ.get('SCRAPERSCONTEXT') == 'staging':
    from staging import *
else: #assume development
    from development import *
	
