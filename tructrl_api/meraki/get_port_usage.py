import json
import os
import time
import subprocess

USAGE_FILE = 'port_usage_by_day.json'
USAGE_REFRESH_SCRIPT = 'get_port_usage_by_day.py'
PORTS_FILE = 'ports.json'
PORTS_REFRESH_SCRIPT = 'get_ports.py'
STALE_SECONDS = 3600  # 1 hour

def is_stale(filename, max_age_seconds):
    if not os.path.exists(filename):
        return True
    file_mtime = os.path.getmtime(filename)
    return (time.time() - file_mtime) > max_age_seconds

if is_stale(USAGE_FILE, STALE_SECONDS):
    print(f"{USAGE_FILE} is missing or stale. Refreshing...")
    subprocess.run(['python', USAGE_REFRESH_SCRIPT], check=True)

if is_stale(PORTS_FILE, STALE_SECONDS):
    print(f"{PORTS_FILE} is missing or stale. Refreshing...")
    subprocess.run(['python', PORTS_REFRESH_SCRIPT], check=True)

# Load the nested ports.json
with open('ports.json', 'r') as f:
    ports = json.load(f)

# Load the usage data
with open('port_usage_by_day.json', 'r') as f:
    usage_data = json.load(f)

# Build a set of used ports: (org, switch, port_id)
used_ports = set()
for org_result in usage_data:
    org = org_result.get('organization')
    usage = org_result.get('usage', {})
    for item in usage.get('items', []):
        switch = item.get('name')
        for port in item.get('ports', []):
            port_id = port.get('portId')
            for interval in port.get('intervals', []):
                usage_vals = (interval.get('data') or {}).get('usage') or {}
                bandwidth_vals = (interval.get('bandwidth') or {}).get('usage') or {}
                energy_vals = (interval.get('energy') or {}).get('usage') or {}
                if any([
                    usage_vals.get('total', 0) != 0 or usage_vals.get('upstream', 0) != 0 or usage_vals.get('downstream', 0) != 0,
                    bandwidth_vals.get('total', 0.0) != 0.0 or bandwidth_vals.get('upstream', 0.0) != 0.0 or bandwidth_vals.get('downstream', 0.0) != 0.0,
                    energy_vals.get('total', 0.0) != 0.0
                ]):
                    used_ports.add((org, switch, str(port_id)))

# Build output in the same nested structure as ports.json, but only with used ports
used_ports_json = {}
used_ports_sums = {}
for org, switches in ports.items():
    for switch, switch_data in switches.items():
        switch_serial = switch_data.get('switch_serial')
        for port in switch_data.get('ports', []):
            port_id = str(port.get('port_id'))
            if (org, switch, port_id) in used_ports:
                if org not in used_ports_json:
                    used_ports_json[org] = {}
                    used_ports_sums[org] = {}
                if switch not in used_ports_json[org]:
                    used_ports_json[org][switch] = {
                        'switch_serial': switch_serial,
                        'ports': []
                    }
                    used_ports_sums[org][switch] = {}
                # Initialize sums for this port
                port_sum = {
                    'port_id': port_id,
                    'port_name': port.get('port_name'),
                    'enabled': port.get('enabled'),
                    'data_total': 0,
                    'data_upstream': 0,
                    'data_downstream': 0,
                    'bandwidth_total': 0.0,
                    'bandwidth_upstream': 0.0,
                    'bandwidth_downstream': 0.0,
                    'energy_total': 0.0
                }
                # Find and sum usage for this port
                for org_result in usage_data:
                    if org_result.get('organization') != org:
                        continue
                    usage = org_result.get('usage', {})
                    for item in usage.get('items', []):
                        if item.get('name') != switch:
                            continue
                        for uport in item.get('ports', []):
                            if str(uport.get('portId')) != port_id:
                                continue
                            for interval in uport.get('intervals', []):
                                usage_vals = (interval.get('data') or {}).get('usage') or {}
                                bandwidth_vals = (interval.get('bandwidth') or {}).get('usage') or {}
                                energy_vals = (interval.get('energy') or {}).get('usage') or {}
                                port_sum['data_total'] += usage_vals.get('total', 0)
                                port_sum['data_upstream'] += usage_vals.get('upstream', 0)
                                port_sum['data_downstream'] += usage_vals.get('downstream', 0)
                                port_sum['bandwidth_total'] += bandwidth_vals.get('total', 0.0)
                                port_sum['bandwidth_upstream'] += bandwidth_vals.get('upstream', 0.0)
                                port_sum['bandwidth_downstream'] += bandwidth_vals.get('downstream', 0.0)
                                port_sum['energy_total'] += energy_vals.get('total', 0.0)
                used_ports_json[org][switch]['ports'].append(port_sum)

with open('port_usage.json', 'w') as f:
    json.dump(used_ports_json, f, indent=2)

# Build output in the same nested structure as ports.json, but only with unused ports
unused_ports_json = {}
for org, switches in ports.items():
    for switch, switch_data in switches.items():
        switch_serial = switch_data.get('switch_serial')
        for port in switch_data.get('ports', []):
            port_id = str(port.get('port_id'))
            if (org, switch, port_id) not in used_ports:
                if org not in unused_ports_json:
                    unused_ports_json[org] = {}
                if switch not in unused_ports_json[org]:
                    unused_ports_json[org][switch] = {
                        'switch_serial': switch_serial,
                        'ports': []
                    }
                unused_ports_json[org][switch]['ports'].append(port)

with open('port_usage_unused.json', 'w') as f:
    json.dump(unused_ports_json, f, indent=2)

import csv

# Dump used ports to CSV
with open('port_usage.csv', 'w', newline='') as csvfile:
    fieldnames = [
        'organization', 'switch', 'switch_serial', 'port_id', 'port_name', 'enabled',
        'data_total', 'data_upstream', 'data_downstream',
        'bandwidth_total', 'bandwidth_upstream', 'bandwidth_downstream',
        'energy_total'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for org, switches in used_ports_json.items():
        for switch, switch_data in switches.items():
            switch_serial = switch_data.get('switch_serial')
            for port in switch_data.get('ports', []):
                row = {
                    'organization': org,
                    'switch': switch,
                    'switch_serial': switch_serial,
                    'port_id': port.get('port_id'),
                    'port_name': port.get('port_name'),
                    'enabled': port.get('enabled'),
                    'data_total': port.get('data_total'),
                    'data_upstream': port.get('data_upstream'),
                    'data_downstream': port.get('data_downstream'),
                    'bandwidth_total': port.get('bandwidth_total'),
                    'bandwidth_upstream': port.get('bandwidth_upstream'),
                    'bandwidth_downstream': port.get('bandwidth_downstream'),
                    'energy_total': port.get('energy_total')
                }
                writer.writerow(row)

# Dump unused ports to CSV
with open('port_usage_unused.csv', 'w', newline='') as csvfile:
    fieldnames = [
        'organization', 'switch', 'switch_serial', 'port_id', 'port_name', 'enabled'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for org, switches in unused_ports_json.items():
        for switch, switch_data in switches.items():
            switch_serial = switch_data.get('switch_serial')
            for port in switch_data.get('ports', []):
                row = {
                    'organization': org,
                    'switch': switch,
                    'switch_serial': switch_serial,
                    'port_id': port.get('port_id'),
                    'port_name': port.get('port_name'),
                    'enabled': port.get('enabled')
                }
                writer.writerow(row)
