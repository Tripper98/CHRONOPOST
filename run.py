###############################################################################
#                            RUN MAIN                                         #
###############################################################################

from application.dashScript import app
from settings import config

app.run_server(debug=config.debug, host=config.host, port=config.port)