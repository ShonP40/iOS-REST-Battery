from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import json
import time
import socket
import errno
from socketserver import ThreadingMixIn

def get_percentage():
    return run_cmd('batterydata | grep "Current Capacity" | awk \'{print $4}\'').strip()

def get_charging_status():
    status = run_cmd('batterydata | grep "Is Charging" | awk \'{print $4}\'').strip()
    return "Charging" if status == '1' else "NotCharging"

def run_cmd(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable='/var/jb/bin/sh')
    start = time.time()

    while True:
        ret = proc.poll()
        if ret is not None:
            out, _ = proc.communicate()
            try:
                return out.decode('utf-8')
            except OSError:
                return ''
        if time.time() - start > 5:
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
            return out.decode('utf-8') if out else ''
        time.sleep(0.1)

class serverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/status':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                body = json.dumps({'Battery': get_percentage(), 'Battery status': get_charging_status()})
                safe_write(self.wfile, body)
            else:
                self.send_error(404)
        except KeyboardInterrupt:
            return
        except socket.error as e:
            try:
                err_no = e.errno
            except AttributeError:
                try:
                    err_no = e[0]
                except Exception:
                    err_no = None
            if err_no == errno.EPIPE:
                return
            return
        except IOError as e:
            try:
                err_no = e.errno
            except AttributeError:
                try:
                    err_no = e[0]
                except Exception:
                    err_no = None
            if err_no == errno.EPIPE:
                return
            return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    daemon_threads = True


def safe_write(wfile, data):
    """Write to wfile and ignore EPIPE/Broken pipe errors (client disconnected).

    wfile is the socket-like file object (self.wfile). data should be a str
    (text).
    """
    try:
        wfile.write(data.encode('utf-8'))
    except socket.error as e:
        err_no = None
        try:
            err_no = e.errno
        except Exception:
            try:
                idx = e[0]
                if isinstance(idx, int):
                    err_no = idx
            except Exception:
                err_no = None
        if err_no == errno.EPIPE:
            return
        raise

def main():
    server = ThreadedHTTPServer(('0.0.0.0', 8000), serverHandler)
    print('Starting server, use <Ctrl-C> to stop')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Shutting down server')
        try:
            server.shutdown()
        except Exception:
            try:
                server.socket.close()
            except Exception:
                pass
        try:
            server.server_close()
        except Exception:
            pass

if __name__ == '__main__':
    main()