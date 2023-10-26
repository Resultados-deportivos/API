import http.server
import socketserver
import json
import psycopg2

# Define the database connection parameters
db_params = {
    "host": "pgsql03.dinaserver.com",
    "database": "eusko_basket",
    "user": "admin_basket",
    "password": "Dinahosting2209@"
}

# Schema name
schema_name = "public"

# Create a function to retrieve data from all tables in the schema
def retrieve_all_tables():
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Get a list of table names in the specified schema
        cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema_name}';")
        table_names = [row[0] for row in cursor.fetchall()]

        data = {}
        for table_name in table_names:
            cursor.execute(f"SELECT * FROM {schema_name}.{table_name}")
            rows = cursor.fetchall()
            data[table_name] = rows

        return data
    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")
        return None
    finally:
        if connection:
            cursor.close()
            connection.close()

# Define the request handler
class MyHandler(http.server.BaseHTTPRequestHandler):
    def _set_response(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = json.loads(post_data.decode('utf-8'))

        data = retrieve_all_tables()
        if data is not None:
            response = {'message': 'Data retrieved successfully', 'data': data}
        else:
            response = {'message': 'Error retrieving data'}

        self._set_response()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = json.loads(post_data.decode('utf-8'))

        data = retrieve_all_tables()
        if data is not None:
            response = {'message': 'Data retrieved successfully', 'data': data}
        else:
            response = {'message': 'Error retrieving data'}

        self._set_response()
        self.wfile.write(json.dumps(response).encode('utf-8'))

# Define the server parameters
host = 'localhost'
port = 8000

with socketserver.TCPServer((host, port), MyHandler) as httpd:
    print(f'Serving at http://{host}:{port}')
    httpd.serve_forever()
