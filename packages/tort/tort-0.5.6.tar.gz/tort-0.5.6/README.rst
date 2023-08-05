Tort
====

Tornado framework helpers.

Requires **Python 3.7+** as it uses contextvars and **Tornado 6+**.

Use cases
=========

Add Request Id to all requests
------------------------------

.. code-block:: python
    import logging
    import tornado.ioloop
    import tornado.web
    from tort.logger import configure_logging

    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            self.write("Hello, world")

    def make_app():
        configure_logging('/tmp/logs_with_request_id.txt', logging.DEBUG)

        return tornado.web.Application([
            (r"/", MainHandler),
        ])

    if __name__ == "__main__":
        app = make_app()
        app.listen(8888)
        tornado.ioloop.IOLoop.current().start()
