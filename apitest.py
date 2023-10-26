import http.server
import socketserver
import json
import psycopg2
import threading

# Define the database connection parameters
db_params = {
    "host": "pgsql03.dinaserver.com:5432",
    "database": "eusko_basket",
    "user": "admin_basket",
    "password": "Dinahosting2209@"
}

# Create a function to query the database and return the result
def query_database(query):
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
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
        # Handle GET requests
        if self.path == "/":
            # Serve the HTML form
            self._set_response(content_type='text/html')
            with open("venv/index.html", "rb") as file:
                self.wfile.write(file.read())
        else:
            self._set_response()
            response = {'message': 'Hello, this is a simple API! (GET)'}
            self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        # Handle POST requests
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = json.loads(post_data.decode('utf-8'))

        if 'query' in post_data:
            query = post_data['query']
            database_result = query_database(query)
            if database_result is not None:
                response = {'message': 'Query executed successfully', 'data': database_result}
                # Save the query result to a JSON file
                with open('result.json', 'w') as json_file:
                    json.dump(database_result, json_file)
            else:
                response = {'message': 'Error executing the query'}
        else:
            response = {'message': 'No query provided'}

        self._set_response()
        self.wfile.write(json.dumps(response).encode('utf-8'))

# Define the server parameters
host = 'localhost'
api_port = 8000
json_port = 8001

# Start the main server and JSON server in separate threads
api_server = socketserver.TCPServer((host, api_port), MyHandler)

def start_json_server():
    json_server = socketserver.TCPServer((host, json_port), http.server.SimpleHTTPRequestHandler)
    json_server.serve_forever()

json_thread = threading.Thread(target=start_json_server)
json_thread.start()

with api_server:
    print(f'API server is running at http://{host}:{api_port}')
    api_server.serve_forever()
