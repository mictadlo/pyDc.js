import os
import json
import motor
import tornado.web
import tornado.ioloop

from bson import json_util  # bson is installed along with pymongo
from tornado import gen


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self):
        self.render('index.html')


class NDXHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self):
        db = self.settings['db']

        cursor = db.things.find({}, fields={'_id': False}).sort('_id')

        data = yield motor.Op(cursor.to_list)

        response_str = json.dumps(data, default=json_util.default)

        self.set_header('Content-Type', 'application/json')
        self.write(response_str)
        self.finish()


if __name__ == '__main__':
    db = motor.MotorClient().open_sync().test

    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler), (r'/ndx', NDXHandler)],
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True, db=db)

    app.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
