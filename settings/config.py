import os



## App settings
name = "Driouche App"

host = "127.0.0.1"

port = int(os.environ.get("PORT", 8050))

debug = True

contacts = "https://www.linkedin.com/in/adnane-driouche-275763177/"

code = "#"

fontawesome = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'



## File system
root = os.path.dirname(os.path.dirname(__file__)) + "/"



## DB