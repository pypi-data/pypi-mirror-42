from flask_simpleapi.core.simple_api import SimpleApi
from flask_simpleapi.core.response import JsonResponse, errors_handler
from flask_mongoengine import MongoEngine
from flask_cors import CORS

import apis


app = SimpleApi(__name__, api_root_path='/api', template_folder='.')

app.config.from_object('settings')

app.response_class = JsonResponse

# Add MongoEngine
MongoEngine(app)

# Add CORS
CORS(app)

# Register app exceptions handlers
for error_code in app.config['HANDLED_ERRORS']:
    app.register_error_handler(error_code, errors_handler)

app.register_apis(apis)
app.print_urls()
