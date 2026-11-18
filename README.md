# BCTracker

A GTFS schedule browser and realtime bus tracker for transit in BC.

Available at https://bctracker.ca

## Agencies

- BC Ferries
- BC Transit
- Denman Island Bus
- Gertie
- Hornby Bus
- Tofino Free Shuttle

## Systems

- 100 Mile House
- BC Ferries
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
- Tofino
- Victoria
- West Coast
- West Kootenay
- Whistler
- Williams Lake

## ABTracker

The site can also be configured to run for Alberta agencies instead of British Columbia.

Available at https://abtracker.ca

The following agencies/systems are supported:

- Calgary Transit (Calgary)
- Edmonton Transit Service (Edmonton)
- Grande Prairie Transit (Grande Prairie)
- Lethbridge Transit (Lethbridge) - No realtime
- Medicine Hat Transit (Medicine Hat)
- Red Deer Transit (Red Deer) - No realtime
- Roam (Banff)
- Woosh (Fort McMurray)

For more information about running the site as ABTracker, see the Basic Configuration section below.

## Running the Project

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

## Server Configuration

In order to run the project, some configuration needs to be set up first.
Start by creating a file in the home directory called `server.conf`, with the following sample content:

```
[global]
server.socket_port: 8080
server.socket_host: '0.0.0.0'
log.error_file: 'logs/serv_log.log'
```

## Feature Configuration

Configure the project's features by creating a `.env` file in the home directory and adding the desired properties from the following sections.

### Basic Configuration

To run the site as ABTracker, set the province code to `AB`.
By default the code is `BC`, which can also be set manually if desired.

```
PROVINCE_CODE=AB
```

If you plan on running multiple instances of BCTracker, you can set a unique cron ID to ensure cron jobs get removed properly per individual server.
By default this ID is `bctracker-muncher`.

```
CRON_ID=<some-unique-id>
```

A secret key can be configured to access the `/admin` page.
When configured, you must go to `/admin?admin_key=<key>` in order to access server management tools.
To enable this, add the following to the configuration file:

```
ADMIN_KEY=<key>
```

Some ferry-based agencies use AIS data instead of normal GTFS realtime.
This can be enabled using the BCTracker AIS project (sold separately).
When it's set up, you can point this project to the data files with this config:

```
AIS_PATH=<path>
```

### Domain Configuration

The current system or agency is determined using the relevant query strings (`system` and `agency`).
For basic setup, no additional configuration is required - everything will simply work out of the box.

The program can work with subdomains for each system/agency, as deployed on our server.
This means that instead of urls like `https://bctracker.ca/routes?system=victoria` you instead have `https://victoria.bctracker.ca/routes`

To enable this you need these config lines, along with the proper DNS and proxying rules.

```
ROOT_DOMAIN="https://example.com/{0}"
SYSTEM_DOMAIN="https://{0}.example.com/{1}"
AGENCY_DOMAIN="https://{0}.example.com/{1}"
COOKIE_DOMAIN=example.com
```

### Key Configuration

If analytics is enabled (see below), a Google Analytics tag must be included:

```
ANALYTICS_KEY=<key>
```

### Functionality Configuration

Some functionality can be enabled or disabled through the configuration.
These properties are defined as `ENABLE_<functionality>` with values of `true` or `false`.
If not included, all functionality defaults to `true`.

The following functionality toggles are currently available:
- `ANALYTICS`
- `GTFS_BACKUPS`
- `REALTIME_BACKUPS`
- `DATABASE_BACKUPS`

Here's an example of what this configuration may look like:

```
ENABLE_GTFS_BACKUPS=false
ENABLE_REALTIME_BACKUPS=false
ENABLE_DATABASE_BACKUPS=true
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
