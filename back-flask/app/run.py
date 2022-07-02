# debug with ipdb usage:
#import ipdb # https://pypi.org/project/ipdb/
#ipdb.set_trace()

# Run a test server.
from app import app
app.run(host='0.0.0.0', port=5000, debug=False)