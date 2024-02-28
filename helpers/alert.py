
from datetime import datetime

from models.alert import Alert, AlertTarget

import database

import protobuf.data.gtfs_realtime_pb2 as protobuf

def create(system, id, data):
    system_id = getattr(system, 'id', system)
    try:
        periods = []
        for period in data.active_period:
            if period.HasField('start'):
                start = datetime.fromtimestamp(period.start).strftime('%B %-d, %Y at %H:%M')
            else:
                start = None
            if period.HasField('end'):
                end = datetime.fromtimestamp(period.end).strftime('%B %-d, %Y at %H:%M')
            else:
                end = None
            if start and end:
                periods.append(f'{start} to {end}')
            elif start:
                periods.append(f'Beginning {start}')
            elif end:
                periods.append(f'Until {end}')
        if periods:
            active_periods = ', '.join(periods)
        else:
            active_periods = None
    except:
        active_periods = None
    try:
        cause = protobuf._ALERT_CAUSE.values_by_number[data.cause].name
    except:
        cause = None
    try:
        effect = protobuf._ALERT_EFFECT.values_by_number[data.effect].name
    except:
        effect = None
    try:
        severity = data.severity
    except:
        severity = None
    try:
        title = data.header_text.translation[0].text
    except:
        title = None
    try:
        description = data.description_text.translation[0].text
    except:
        description = None
    database.insert('alert', {
        'system_id': system_id,
        'alert_id': id,
        'active_periods': active_periods,
        'cause': cause,
        'effect': effect,
        'severity': severity,
        'title': title,
        'description': description
    })
    for entity in data.informed_entity:
        if entity.HasField('route_id'):
            route_id = entity.route_id
        else:
            route_id = None
        if entity.HasField('stop_id'):
            stop_id = entity.stop_id
        else:
            stop_id = None
        if entity.HasField('trip'):
            trip_id = entity.trip.trip_id
        else:
            trip_id = None
        database.insert('alert_target', {
            'system_id': system_id,
            'alert_id': id,
            'route_id': route_id,
            'stop_id': stop_id,
            'trip_id': trip_id
        })

def find_all(system, route=None, stop=None, trip=None):
    system_id = getattr(system, 'id', system)
    route_id = getattr(route, 'id', route)
    stop_id = getattr(stop, 'id', stop)
    trip_id = getattr(trip, 'id', trip)
    cte, args = database.build_select('alert_target',
        columns={
            'system_id': 'system_id',
            'alert_id': 'alert_id'
        },
        distinct=True,
        filters={
            'system_id': system_id,
            'route_id': route_id,
            'stop_id': stop_id,
            'trip_id': trip_id
        }
    )
    return database.select('filtered_alert',
        columns={
            'alert.system_id': 'alert_system_id',
            'alert.alert_id': 'alert_id',
            'alert.active_periods': 'alert_active_periods',
            'alert.cause': 'alert_cause',
            'alert.effect': 'alert_effect',
            'alert.severity': 'alert_severity',
            'alert.title': 'alert_title',
            'alert.description': 'alert_description'
        },
        ctes={
            'filtered_alert': cte
        },
        joins={
            'alert': {
                'alert.system_id': 'filtered_alert.system_id',
                'alert.alert_id': 'filtered_alert.alert_id'
            }
        },
        custom_args=args,
        initializer=Alert.from_db
    )

def find_all_targets(system, route=None, stop=None, trip=None):
    system_id = getattr(system, 'id', system)
    route_id = getattr(route, 'id', route)
    stop_id = getattr(stop, 'id', stop)
    trip_id = getattr(trip, 'id', trip)
    return database.select('alert_target',
        columns={
            'alert_target.system_id': 'alert_target_system_id',
            'alert_target.alert_id': 'alert_target_alert_id',
            'alert_target.route_id': 'alert_target_route_id',
            'alert_target.stop_id': 'alert_target_stop_id',
            'alert_target.trip_id': 'alert_target_trip_id',
        },
        filters={
            'alert_target.system_id': system_id,
            'alert_target.route_id': route_id,
            'alert_target.stop_id': stop_id,
            'alert_target.trip_id': trip_id
        },
        initializer=AlertTarget.from_db
    )

def delete_all(system):
    system_id = getattr(system, 'id', system)
    database.delete('alert', {
        'system_id': system_id
    })
    database.delete('alert_target', {
        'system_id': system_id
    })
