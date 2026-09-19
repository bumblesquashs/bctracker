
CREATE TABLE IF NOT EXISTS allocation (
    allocation_id INTEGER PRIMARY KEY ASC,
    agency_id TEXT NOT NULL,
    vehicle_id TEXT NOT NULL,
    system_id TEXT,
    first_seen TEXT NOT NULL,
    last_seen TEXT NOT NULL,
    active INTEGER NOT NULL,
    last_lat REAL,
    last_lon REAL,
    last_stop_id TEXT,
    last_stop_number TEXT,
    last_stop_name TEXT,
    last_seen_timestamp REAL
);

CREATE TABLE IF NOT EXISTS record (
    record_id INTEGER PRIMARY KEY ASC,
    allocation_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    block_id TEXT,
    route_numbers TEXT,
    start_time TEXT,
    end_time TEXT,
    first_seen TEXT,
    last_seen TEXT,
    FOREIGN KEY (allocation_id) REFERENCES allocation (allocation_id)
);

CREATE TABLE IF NOT EXISTS trip_record (
    trip_record_id INTEGER PRIMARY KEY ASC,
    record_id INTEGER NOT NULL,
    trip_id TEXT NOT NULL,
    FOREIGN KEY (record_id) REFERENCES record (record_id)
);

CREATE TABLE IF NOT EXISTS allocation_record (
    allocation_id INTEGER UNIQUE NOT NULL,
    first_record_id INTEGER,
    last_record_id INTEGER,
    FOREIGN KEY (allocation_id) REFERENCES allocation (allocation_id),
    FOREIGN KEY (first_record_id) REFERENCES record (record_id),
    FOREIGN KEY (last_record_id) REFERENCES record (record_id)
);

CREATE TABLE IF NOT EXISTS transfer (
    transfer_id INTEGER PRIMARY KEY ASC,
    date TEXT NOT NULL,
    old_allocation_id INTEGER NOT NULL,
    new_allocation_id INTEGER NOT NULL,
    FOREIGN KEY (old_allocation_id) REFERENCES allocation (allocation_id),
    FOREIGN KEY (new_allocation_id) REFERENCES allocation (allocation_id)
);

CREATE TABLE IF NOT EXISTS position (
    agency_id TEXT NOT NULL,
    vehicle_id TEXT NOT NULL,
    system_id TEXT,
    trip_id TEXT,
    stop_id TEXT,
    block_id TEXT,
    route_id TEXT,
    sequence INTEGER,
    lat REAL,
    lon REAL,
    bearing REAL,
    speed INTEGER,
    adherence INTEGER,
    layover INTEGER,
    occupancy TEXT,
    timestamp REAL,
    PRIMARY KEY (agency_id, vehicle_id)
);

CREATE TABLE IF NOT EXISTS assignment (
    block_id TEXT NOT NULL,
    allocation_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    PRIMARY KEY (block_id, allocation_id),
    FOREIGN KEY (allocation_id) REFERENCES allocation (allocation_id)
);

CREATE TABLE IF NOT EXISTS download (
    download_id INTEGER PRIMARY KEY ASC,
    agency_id TEXT NOT NULL,
    system_id TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    trigger TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS route (
    download_id TEXT NOT NULL,
    route_id TEXT NOT NULL,
    number TEXT NOT NULL,
    name TEXT NOT NULL,
    colour TEXT,
    text_colour TEXT,
    type TEXT,
    sort_order INTEGER,
    PRIMARY KEY (download_id, route_id)
);

CREATE TABLE IF NOT EXISTS stop (
    download_id TEXT NOT NULL,
    stop_id TEXT NOT NULL,
    number TEXT NOT NULL,
    name TEXT NOT NULL,
    lat REAL NOT NULL,
    lon REAL NOT NULL,
    parent_id TEXT,
    type TEXT,
    PRIMARY KEY (download_id, stop_id)
);

CREATE TABLE IF NOT EXISTS trip (
    download_id TEXT NOT NULL,
    trip_id TEXT NOT NULL,
    route_id TEXT NOT NULL,
    service_id TEXT NOT NULL,
    block_id TEXT,
    direction_id INTEGER,
    shape_id TEXT,
    headsign TEXT NOT NULL,
    PRIMARY KEY (download_id, trip_id),
    FOREIGN KEY (download_id, route_id) REFERENCES route (download_id, route_id)
);

CREATE TABLE IF NOT EXISTS departure (
    download_id TEXT NOT NULL,
    trip_id TEXT NOT NULL,
    sequence INTEGER NOT NULL,
    stop_id TEXT NOT NULL,
    time TEXT NOT NULL,
    pickup_type TEXT NOT NULL,
    dropoff_type TEXT NOT NULL,
    timepoint INTEGER NOT NULL,
    distance REAL,
    headsign TEXT,
    PRIMARY KEY (download_id, trip_id, sequence),
    FOREIGN KEY (download_id, trip_id) REFERENCES trip (download_id, trip_id),
    FOREIGN KEY (download_id, stop_id) REFERENCES stop (download_id, stop_id)
);

CREATE TABLE IF NOT EXISTS point (
    download_id TEXT NOT NULL,
    shape_id TEXT NOT NULL,
    sequence INTEGER NOT NULL,
    lat REAL NOT NULL,
    lon REAL NOT NULL,
    PRIMARY KEY (download_id, shape_id, sequence)
);

CREATE INDEX IF NOT EXISTS allocation_agency_vehicle ON allocation (agency_id, vehicle_id);
CREATE INDEX IF NOT EXISTS record_allocation ON record (allocation_id);
CREATE INDEX IF NOT EXISTS trip_record_record_id ON trip_record (record_id);
CREATE INDEX IF NOT EXISTS transfer_old_allocation ON transfer (old_allocation_id);
CREATE INDEX IF NOT EXISTS transfer_new_allocation ON transfer (new_allocation_id);
CREATE INDEX IF NOT EXISTS departure_trip_id ON departure (trip_id);
CREATE INDEX IF NOT EXISTS departure_stop_id ON departure (stop_id);
