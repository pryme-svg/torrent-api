# torrent_api

A torrent scraper and API written in python

A working instance can be found at https://torrent-api1.herokuapp.com/

## Example

https://torrent-api1.herokuapp.com/getTorrents?site=1337x&query=witcher

Returns torrents for witcher

## Running

Install dependencies

```
pip install -r requirements.txt
```

Run the server

```
gunicorn wsgi:app
```
