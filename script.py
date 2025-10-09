from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import subprocess
import simplejson as json
import time

def get_percentage():
    return run_cmd('batterydata | grep "Current Capacity" | awk \'{print $4}\'', timeout=5).strip()

def get_charging_status():
    status = run_cmd('batterydata | grep "Is Charging" | awk \'{print $4}\'', timeout=5).strip()
    return "Charging" if status == '1' else "NotCharging"

def run_cmd(cmd, timeout):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    start = time.time()

    while True:
        ret = proc.poll()
        if ret is not None:
            out, _ = proc.communicate()
            try:
                return out
            except OSError:
                return ''
        if time.time() - start > timeout:
            try:
                proc.terminate()
            except (OSError, AttributeError):
                pass
            time.sleep(0.1)
            if proc.poll() is None:
                try:
                    proc.kill()
                except (OSError, AttributeError):
                    pass
            out, _ = proc.communicate()
            return out or ''
        time.sleep(0.1)

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