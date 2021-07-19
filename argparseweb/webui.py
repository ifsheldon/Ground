import web

from . import page

import multiprocess as multiprocessing

import webbrowser

config_file = "a.json"

class Webui(object):
  def __init__(self, parser, title="Argparse Web UI"):
    self._parser = parser
    self._title = title

  def get_urls(self):
    return ('/', 'index')

  def app(self, dispatch, parsed):
    # Make sure we get an argh-like object here that has a dispatch object
    if dispatch is None:
      if not hasattr(self._parser, 'dispatch'):
        raise ValueError("Can't dispatch a non dispatchable parser without a dispatch method")
      dispatch = self._parser.dispatch
      parsed = False

    class WebuiPageWrapper(page.WebuiPage):
      _parser = self._parser
      _dispatch = dispatch
      _parsed = parsed
      _title = self._title

    class JsonHandler:
      def __init__(self):
          self.filename = None

      def check_path(self):
          if "json" in web.ctx.fullpath:
            self.filename = config_file
          elif "init" in web.ctx.fullpath:
            self.filename = page.init_file
          

      def GET(self):
          self.check_path()
          
          with open(self.filename,"r", encoding="utf8") as f:
              content = f.readlines()
          return "".join(content)
      
      def POST(self):
          self.check_path()


          print("received:", web.data().decode("utf8"))
          with open(self.filename,"w", encoding="utf8") as f:
              f.write(web.data().decode("utf8"))
          return "written"

    urls = ('/', 'index', '/json', 'JsonHandler', "/init", 'init')
    classes = {'index': WebuiPageWrapper, 'JsonHandler': JsonHandler, 'init': JsonHandler}

    return web.application(urls, classes)

  def dispatch(self, dispatch=None, parsed=False):
    self.app(dispatch=dispatch, parsed=parsed).run()

  def wsgi(self, dispatch=None, parsed=True):
    return self.app(dispatch, parsed).wsgifunc()

  def get(self, count=True):
    # prepare a process-safe queue to hold all results
    results = multiprocessing.Queue()

    # spawn web.py server in another process, have it's dispatch as queue.put method
    app = self.app(dispatch=results.put, parsed=True)
    t = multiprocessing.Process(target=app.run)
    t.start()

    webbrowser.open_new_tab("http://localhost:8080")

    # stop condition: if count is a number decrease and loop until 0,
    #   if count is True, loop forever
    while count:
      yield results.get()

      if type(count) == int:
        count -= 1

    app.stop()
    t.terminate()

  def getone(self):
    return list(self.get(count=1))[0]
