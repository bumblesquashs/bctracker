# BCTracker

A GTFS schedule browser and realtime bus tracker for BC Transit.

Available at https://www.bctracker.ca

## Current Systems

Systems with full support for schedules and bus tracking:
- Campbell River
- Comox Valley
- Cowichan Valley
- Creston Valley
- Dawson Creek
- East Kootenay
- Fort St. John
- Fraser Valley
- Kamloops
- Kelowna
- Kitimat
- Nanaimo
- North Okanagan
- Port Alberni
- Prince George
- Prince Rupert
- Powell River
- South Okanagan
- Squamish
- Sunshine Coast
- Victoria
- West Kootenay
- Whistler

Systems with limited support for bus tracking only:
- Mount Waddington

Additional systems may be added in the future if schedule and/or realtime GTFS becomes available.

## Running the project

Server developed and deployed on Linux (Runs fine on Ubuntu 18+, Mint).
Also has been tested and confirmed to work on macOS.
Not tested on Windows.
Requires roughly Python 3.7 or higher, and pip.

Uses the Bottle framework for web stuff and templates, and maps are done with MapBox.

To run the project, start by creating a file in the home directory called `server.conf`, with the following sample content:

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

The program can work with subdomains for each system, as deployed on our server.
This means that instead of urls like `http://example.com/victoria/routes` you would have `http://victoria.example.com/routes`

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

A secret key can also be configured to access the `/admin` page.
When configured, you must go to `/admin/<key>` in order to access server management tools.
To enable this, add the following to `server.conf`:

```
admin_key: 'some-admin-key'
```

Once you've done that, run `setup.sh` to install packages and create directories, and then run `start.py` to load up the server.
