import hashlib
import hmac
import json
import os
import sys
import tempfile

import distutils.core
import git
import twine.commands.upload

from six.moves import BaseHTTPServer


class PyPI(object):

    @staticmethod
    def release(url, tag):
        with tempfile.TemporaryDirectory() as wd:
            os.chdir(wd)
            repo = git.Repo.clone_from(url, wd)
            repo.git.checkout(tag)
            sys.path.insert(0, wd)
            distutils.core.run_setup(os.path.join(wd, 'setup.py'),
                                     ['sdist', 'bdist_wheel', '--universal'])
            twine.commands.upload.main([os.path.join(wd, 'dist', '*')])


class HTTPServer(object):

    def __init__(self, port):
        class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

            def do_POST(self):
                def verify(signature, data):
                    try:
                        sha, signature = signature.split('=')
                    except ValueError:
                        return False
                    if sha != 'sha1':
                        return False
                    mac = hmac.new(os.environb.get(b'SECRET', bytes()), data, hashlib.sha1)
                    return hmac.compare_digest(mac.hexdigest(), signature)

                length = int(self.headers.get('Content-Length', 0))
                data = self.rfile.read(length)
                if not verify(self.headers.get('X-Hub-Signature'), data):
                    self.send_error(403)
                    return
                event = self.headers.get('X-GitHub-Event')
                if event == 'ping':
                    self.send_response(200)
                    return
                if event == 'release':
                    data = json.loads(data)
                    url = data.get('clone_url')
                    tag = data.get('release', {}).get('tag_name')
                    PyPI.release(url, tag)
                self.send_response(200)

        self.server = BaseHTTPServer.HTTPServer(('', port), RequestHandler)

    def serve(self):
        self.server.serve_forever()


def main():
    try:
        HTTPServer(80).serve()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
