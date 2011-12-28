import os

if os.environ.get('AACONTEXT') == 'production':
    from production import *
elif os.environ.get('AACONTEXT') == 'staging':
    from staging import *
else: #assume development
    from development import *
	
