# BCTracker

A GTFS schedule browser and realtime bus tracker for BC Transit.

Available at https://www.bctracker.ca

## Current Systems

- Campbell River
- Comox Valley
- Cowichan Valley
- Fraser Valley
- Kamloops
- Kelowna
- Nanaimo
- North Okanagan
- Port Alberni
- Prince George
- Powell River
- South Okanagan
- Squamish
- Sunshine Coast
- Victoria
- West Kootenay
- Whistler

More systems coming soon!

## Running the project

Server developed and deployed on linux (Runs fine on Ubuntu 18+, Mint). The code will likely also work on OSX, but probably with some small modifications. Windows is doubtful. Requires roughly python 3.7 or higher, and pip.

Uses the Bottle framework for web stuff and templates, and maps are done with MapBox.

To run the project, create a file in the home directory called `server.conf`, with the following sample content:

```
[global]
server.socket_port: 8080
server.socket_host: '0.0.0.0'
log.error_file: 'logs/serv_log.log'
mapbox_api_key: '<API KEY HERE>'
system_domain: 'http://localhost:8080/{0}/{1}'
no_system_domain: 'http://localhost:8080/{0}'
system_domain_path: 'http://localhost:8080/{0}/{1}'
```

The system can work with subdomains for each system, as deployed on our server. This means that instead of urls like `http://example.com/victoria/routes` you would have `http://victoria.example.com/routes`

To enable this, in `server.conf`, you need these lines instead, along with the proper DNS and proxying rules.

```
system_domain: 'http://{0}.example.com/{1}'
no_system_domain: 'http://example.com/{0}'
system_domain_path: 'http://example.com/{0}/{1}
cookie_domain: 'example.com'
```

If you plan on running multiple instances of BCTracker, you can set a unique cron ID in `server.conf` to ensure cron jobs get removed properly per individual server.

```
cron_id: 'some-unique-id'
```

Once you've done that, run `setup.sh` to install packages and create directories, and then run `start.py` to load up the server.
