from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import subprocess
import simplejson as json

def get_percentage():
    return subprocess.Popen(['batterydata | grep "Current Capacity" | awk \'{print $4}\''], shell=True, stdout=subprocess.PIPE).communicate()[0]

def get_charging_status():
    return subprocess.Popen(['batterydata | grep "Is Charging" | awk \'{print $4}\''], shell=True, stdout=subprocess.PIPE).communicate()[0]

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/percentage':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data = get_percentage()
            self.wfile.write(json.dumps({'info': data}).encode())
        elif self.path == '/charging':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data = get_charging_status()
            self.wfile.write(json.dumps({'info': data}).encode())
        else:
            self.send_error(404)

def main():
    server = HTTPServer(('0.0.0.0', 8000), MyHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()

if __name__ == '__main__':
    main()