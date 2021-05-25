import web

from . import page

import multiprocess as multiprocessing

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
      def GET(self):
          with open("a.json","r", encoding="utf8") as f:
              content = f.readlines()
          return "".join(content)
      
      def POST(self):
          print("received:", web.data().decode("utf8"))
          with open("a.json","w", encoding="utf8") as f:
              f.write(web.data().decode("utf8"))
          return "written"

    urls = ('/', 'index', '/json', 'JsonHandler')
    classes = {'index': WebuiPageWrapper, 'JsonHandler': JsonHandler}

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
