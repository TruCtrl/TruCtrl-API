import os
from dotenv import load_dotenv
import meraki
import json

# Load .env file
load_dotenv()
API_KEY = os.getenv('MERAKI_API_KEY')

if not API_KEY:
    raise ValueError('MERAKI_API_KEY not found in .env file')

# Initialize Meraki Dashboard API

dashboard = meraki.DashboardAPI(API_KEY)

# Get list of organizations
orgs = dashboard.organizations.getOrganizations()

# For each org, get all devices and their switch ports
nested_ports = {}
for org in orgs:
    org_id = org['id']
    org_name = org['name']
    print(f"Organization: {org_name} ({org_id})")
    devices = dashboard.organizations.getOrganizationDevices(org_id)
    for device in devices:
        if device.get('model', '').startswith('MS'):
            switch_name = device['name']
            switch_serial = device['serial']
            print(f"  Switch: {switch_name} ({switch_serial})")
            try:
                ports = dashboard.switch.getDeviceSwitchPorts(switch_serial)
                for port in ports:
                    port_id = port['portId']
                    port_name = port['name']
                    enabled = port['enabled']
                    print(f"    Port {port_id}: {port_name} - Enabled: {enabled}")
                    if org_name not in nested_ports:
                        nested_ports[org_name] = {}
                    if switch_name not in nested_ports[org_name]:
                        nested_ports[org_name][switch_name] = {
                            'switch_serial': switch_serial,
                            'ports': []
                        }
                    nested_ports[org_name][switch_name]['ports'].append({
                        'port_id': port_id,
                        'port_name': port_name,
                        'enabled': enabled
                    })
            except Exception as e:
                print(f"    Error fetching ports: {e}")

# Write output to ports.json
with open('ports.json', 'w') as f:
    json.dump(nested_ports, f, indent=2)