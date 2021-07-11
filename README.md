# BCTracker

A GTFS schedule browser and realtime bus tracker for BC Transit.

Available at http://www.bctracker.ca

Systems with static GTFS and realtime:
- Comox Valley
- Kamloops
- Kelowna
- Nanaimo
- Squamish
- Victoria
- Whistler

Systems with static GTFS only:
- Central Fraser Valley
- Chilliwack
- Fraser Valley Express (integrated with Chilliwack, schedules accessible via Chilliwack and Central Fraser Valley)
- Prince George

More systems coming soon!

## Running the project

Server developed and deployed on linux (Runs fine on Ubuntu 18+, Mint). The code will likely also work on OSX, but probably with some small modifications. Windows is doubtful. Requires roughly python 3.7 or higher, and pip.

Uses the bottle framework for web stuff and templates, and maps are done with mapbox.

To run the project, create a file in the home directory called `server.conf`, with the following sample content:

```
[global]
server.socket_port: 8080
server.socket_host: '0.0.0.0'
log.error_file: 'logs/serv_log.log'
mapbox_api_key: '<API KEY HERE>'
system_domain: 'http://localhost:8080/{0}/{1}'
no_system_domain: 'http://localhost:8080/{0}'

```

The system can work with subdomains for each system, as deployed on our server:
This means that instead of urls like
http://example.com/victoria/routes 
you would have
http://victoria.example.com/routes

To enable this, in server.conf, you need these lines instead, along with the proper DNS and proxying rules.

```
system_domain: 'http://{0}.example.com/{1}'
no_system_domain: 'http://example.com/{0}'
```

Once you've done that, run setup.sh to install packages and create directories, and then run start.py to load up the server.

