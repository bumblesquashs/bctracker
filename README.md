# BCTracker

A GTFS schedule browser and realtime bus tracker for transit in BC.

Available at https://bctracker.ca

## Agencies

- BC Transit
- Denman Island Bus
- Gertie
- Hornby Bus

## Systems

- 100 Mile House
- Ashcroft-Clinton
- Campbell River
- Clearwater
- Comox Valley
- Cowichan Valley
- Creston Valley
- Dawson Creek
- Denman Island
- East Kootenay
- Fort St. John
- Fraser Valley
- Gabriola Island
- Hornby Island
- Kamloops
- Kelowna
- Kitimat-Stikine
- Merritt
- Mount Waddington
- Nanaimo
- North Okanagan
- Pemberton
- Port Alberni
- Prince George
- Prince Rupert
- Powell River
- Quesnel
- Revelstoke
- Salt Spring Island
- Smithers
- South Okanagan
- Squamish
- Sunshine Coast
- Victoria
- West Coast
- West Kootenay
- Whistler
- Williams Lake

## Running the project

Server developed and deployed on Linux (Runs fine on Ubuntu 18+, Mint).
Also has been tested and confirmed to work on macOS.
Not tested on Windows.
Requires roughly Python 3.11 or higher, and pip.

Uses the [Bottle](https://bottlepy.org) framework for web stuff and templates, and maps are done with [OpenLayers](https://openlayers.org).

Before running the server, some configuration needs to be set up first by following the steps in the Configuration section below.
Once you've done that, run `setup.sh` to install packages and create directories, and then run `start.py` to load up the server.

When launching the server, a few flags can be passed in to perform specific actions on startup:

- `--reload` (`-r`) Re-downloads all GTFS data
- `--updatedb` (`-u`) Updates GTFS data in the database with downloaded CSV data (automatically done when `--reload` is used)
- `--debug` (`-d`) Enables debug mode when developing

## Configuration

In order to run the project, some configuration needs to be set up first.
Start by creating a file in the home directory called `server.conf`, with the following sample content:

```
[global]
server.socket_port: 8080
server.socket_host: '0.0.0.0'
log.error_file: 'logs/serv_log.log'
```

Additional configuration, including some required properties, is described in the following sections.

### Basic configuration

If you plan on running multiple instances of BCTracker, you can set a unique cron ID to ensure cron jobs get removed properly per individual server.
By default this ID is `bctracker-muncher`.

```
cron_id: 'some-unique-id'
```

A secret key can be configured to access the `/admin` page.
When configured, you must go to `/admin?admin_key=<key>` in order to access server management tools.
To enable this, add the following to the configuration file:

```
admin_key: '<key>'
```

### Domain configuration

By default, the current system (if any) is included as the first part of the URL path.
In order to ensure all links and references work correctly, config for domains **must** be included before running.

Here's an example of the domain config required in `server.conf`:

```
all_systems_domain: 'http://localhost:8080/{0}'
system_domain: 'http://localhost:8080/{0}/{1}'
system_domain_path: 'http://localhost:8080/{0}/{1}'
```

The program can work with subdomains for each system, as deployed on our server.
This means that instead of urls like `https://bctracker.ca/victoria/routes` you instead have `https://victoria.bctracker.ca/routes`

To enable this you need these lines instead, along with the proper DNS and proxying rules.

```
all_systems_domain: 'http://example.com/{0}'
system_domain: 'http://{0}.example.com/{1}'
system_domain_path: 'http://example.com/{0}/{1}
cookie_domain: 'example.com'
```

### Key Configuration

If analytics is enabled (see below), a Google Analytics tag must be included:

```
analytics_key: '<key>'
```

### Functionality Configuration

Some functionality can be enabled or disabled through the configuration.
These properties are defined as `enable_<functionality>` with values of `'true'` or `'false'`.
If not included, all functionality defaults to `'true'`.

The following functionality toggles are currently available:
- `analytics`
- `gtfs_backups`
- `realtime_backups`
- `database_backups`

Here's an example of what this configuration may look like:

```
enable_gtfs_backups: 'false'
enable_realtime_backups: 'false'
enable_gtfs_backups: 'true'
```

## Certbot wildcard domain renew

To renew a wildcard domain on certbot, you need to do the following:

in the server:

```
certbot certonly --manual --preferred-challenges dns
```

When it asks, enter whatever domain name you are using like so:
```
bctracker.ca, *.bctracker.ca
```

Finally, it give a random string for the "ACME Challenge". You will need to go to your DNS settings and add a TXT record for `_acme-challenge` with the value they provide.
After applying this change, wait some time before hitting enter to continue. Check out a dig tool like this https://toolbox.googleapps.com/apps/dig/#TXT/_acme-challenge.bctracker.ca 
to see whether your new record is showing up. You want it to be showing up over dig so that certbot can read it.

After hitting enter, it may ask you to set ANOTHER TXT record too also under `_acme-challenge` which is apparently just fine. Same procedure. Hopefully after that, it will have worked.

After cerbot runs, don't forget to hit `service nginx reload`!! And then all will be good.
