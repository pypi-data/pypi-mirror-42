import json
import os
import os.path
import nbformat
from notebook.base.handlers import IPythonHandler
from notebook.utils import url_path_join
try:
    from backports.tempfile import TemporaryDirectory
except ImportError:
    from tempfile import TemporaryDirectory

from .tests import runWithHTMLReturn


class RunCelltestsHandler(IPythonHandler):
    def initialize(self):
        pass

    def get(self):
        self.finish({'status': 0, 'test': ''})

    def post(self):
        body = json.loads(self.request.body)
        path = os.path.join(os.getcwd(), body.get('path'))
        name = path.rsplit('/', 1)[1]
        with TemporaryDirectory() as tempdir:
            path = os.path.abspath(os.path.join(tempdir, name))
            node = nbformat.from_dict(body.get('model'))
            nbformat.write(node, path)
            ret = runWithHTMLReturn(path)
            self.finish({'status': 0, 'test': ret})


def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app

    host_pattern = '.*$'
    base_url = web_app.settings['base_url']
    # host_pattern = '.*$'
    print('Installing jupyterlab_celltests handler on path %s' % url_path_join(base_url, 'celltests'))

    web_app.add_handlers(host_pattern, [(url_path_join(base_url, 'celltests/run'), RunCelltestsHandler, {})])
