import os
from dotenv import load_dotenv
import meraki
import json
from datetime import datetime, timedelta

# Load .env file
load_dotenv()
API_KEY = os.getenv('MERAKI_API_KEY')

if not API_KEY:
    raise ValueError('MERAKI_API_KEY not found in .env file')

# Initialize Meraki Dashboard API
dashboard = meraki.DashboardAPI(API_KEY)

# Get list of organizations
orgs = dashboard.organizations.getOrganizations()

# For each org, get switch ports usage history by device by interval
usage_output = []
for org in orgs:
    org_id = org['id']
    print(f"Organization: {org['name']} ({org_id})")
    try:
        all_items = []
        starting_after = None
        while True:
            params = {
                'timespan': 2678400,
                'interval': 86400,
                'perPage': 50
            }
            if starting_after:
                params['startingAfter'] = starting_after
            usage = dashboard.switch.getOrganizationSwitchPortsUsageHistoryByDeviceByInterval(
                org_id,
                **params
            )
            items = usage.get('items', [])
            all_items.extend(items)
            meta = usage.get('meta', {})
            counts = meta.get('counts', {}).get('items', {})
            remaining = counts.get('remaining', 0)
            # Pagination: continue if remaining > 0
            if not items or remaining == 0:
                break
            # Use last item's serial as startingAfter if present
            last_item = items[-1]
            if 'serial' in last_item:
                starting_after = last_item['serial']
            else:
                # If no serial, break to avoid infinite loop
                break
        usage_output.append({
            'organization': org['name'],
            'organization_id': org_id,
            'usage': {'items': all_items}
        })
    except Exception as e:
        usage_output.append({
            'organization': org['name'],
            'organization_id': org_id,
            'error': str(e)
        })

# Filter out intervals with all zero usage, bandwidth, and energy
def has_nonzero_usage(interval):
    usage = (interval.get('data') or {}).get('usage') or {}
    bandwidth = (interval.get('bandwidth') or {}).get('usage') or {}
    energy = (interval.get('energy') or {}).get('usage') or {}
    return any([
        usage.get('total', 0) != 0 or usage.get('upstream', 0) != 0 or usage.get('downstream', 0) != 0,
        bandwidth.get('total', 0.0) != 0.0 or bandwidth.get('upstream', 0.0) != 0.0 or bandwidth.get('downstream', 0.0) != 0.0,
        energy.get('total', 0.0) != 0.0
    ])

# Clean usage data before saving
for org_result in usage_output:
    if 'usage' in org_result and 'items' in org_result['usage']:
        for item in org_result['usage']['items']:
            if 'ports' in item:
                for port in item['ports']:
                    if 'intervals' in port:
                        port['intervals'] = [interval for interval in port['intervals'] if has_nonzero_usage(interval)]

# Write output to ports_usage_by_day.json
with open('port_usage_by_day.json', 'w') as f:
    json.dump(usage_output, f, indent=2)
