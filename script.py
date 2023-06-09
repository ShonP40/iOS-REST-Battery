from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import subprocess
import simplejson as json

def get_percentage():
    return (subprocess.Popen(['batterydata | grep "Current Capacity" | awk \'{print $4}\''], shell=True, stdout=subprocess.PIPE).communicate()[0]).strip()

def get_charging_status():
    status = (subprocess.Popen(['batterydata | grep "Is Charging" | awk \'{print $4}\''], shell=True, stdout=subprocess.PIPE).communicate()[0]).strip()

    return "Charging" if status == '1' else "NotCharging"

class serverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'Battery': get_percentage(), 'Battery status': get_charging_status()}).encode())
        else:
            self.send_error(404)

def main():
    server = HTTPServer(('0.0.0.0', 8000), serverHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()

if __name__ == '__main__':
    main()