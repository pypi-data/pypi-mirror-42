
This package implements stand-alone REST API server to manage Xena Valkyrie chassis.

Functionality
"""""""""""""
Full REST API with functionality equivalent to the CLI. 

Installation
""""""""""""
pip instsll xenavalkyrie-rest

Getting started
"""""""""""""""
Start the server
----------------
gunicorn2 xenavalkyrie_rest.wsgi:app -c xenavalkyrie_rest/settings.py

Start the development server
----------------------------
./xena_rest_server.py

Documentation
"""""""""""""

Xena CLI does not distinguish between attributes, operations and statistics. All are flat, unstructured, commands.

Each object has the following sub-routes - commands, attributes, statistics, operations.
Note that for some objects some of the sub-routes are not applicable and in this case the sub-route is missing.

Commands:
- Any raw CLI command.

The following sub-routes are abstractions on top of the raw CLI commands represented in the commands sub-route.

Attributes:
- Returns all attributes in one call as dictionary
- Allows set of group of attributes

Statistics:
- Structured statistics.

Operations:
- Strcutured operations. Not supported in first release.

CLI documentation - 
swagger UI - http://<SERVER>:<PORT>/api
swagger version 2.0 JSON - http://<SERVER>:<PORT>/api/swagger.json

Related works
"""""""""""""
xenavalkyrie

Contact
"""""""
Feel free to contact me with any question or feature request at yoram@ignissoft.com
