import json
import tornado.ioloop
import tornado.web
import scraper

class Torrents(tornado.web.RequestHandler):
    def prepare(self):
        header = "Content-Type"
        body = "application/json"
        self.set_header(header, body)

    async def get(self):
        query = self.get_argument('query', None)
        site = self.get_argument('site', None)
        try:
            site
        except NameError:
            site = "1337x"
        if query is None:
            raise tornado.web.HTTPError(400)
        if site == "1337x":
            data = json.dumps({"torrents": await scraper.search1337x(query)})
        elif site == "nyaa":
            data = json.dumps({"torrents": await scraper.searchNyaa(query)})
        elif site == "Rarbg":
            data = json.dumps({"torrents": await scraper.searchRarbg(query)})
        elif site == "tpb":
            data = json.dumps({"torrents": await scraper.searchTPB(query)})
        else:
            data = json.dumps({"torrents": await scraper.search1337x(query)})
        self.write(data)

class Info(tornado.web.RequestHandler):
    def prepare(self):
        header = "Content-Type"
        body = "application/json"
        self.set_header(header, body)    

    async def get(self):
        gh = "https://github.com/pryme-svg/torrent-api"
        sites = ["1337x", "tpb", "Ettvdl", "Rarbg", 'nyaa']
        data = json.dumps({"github": gh, "sites": sites})
        self.write(data)

if __name__ == '__main__':
    app = tornado.web.Application([ (r'/getTorrents', Torrents), (r'/', Info) ])
    port = int(os.environ.get("PORT", 5000))
    app.listen(port)
    print('Starting server on port {}'.format(port))
    tornado.ioloop.IOLoop.instance().start()
