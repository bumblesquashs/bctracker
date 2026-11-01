#!/usr/bin/env python

import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from database import Database

database = Database()
database.connect()

database.execute("DROP TABLE position")
database.execute("ALTER TABLE allocation ADD last_seen_source TEXT")

database.update(
    table="allocation",
    values={
        "last_seen_source": "gtfs"
    },
    filters={
        "agency_id": "bc-transit"
    }
)
database.update(
    table="allocation",
    values={
        "last_seen_source": "ais"
    },
    filters={
        "agency_id": "bc-ferries"
    }
)

database.commit()
database.disconnect()
