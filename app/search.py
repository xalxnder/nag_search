import requests
import json
from .keys import nagiosKeys, generate_url_hosts, generate_url_services

matches = []
NO_MATCHES = []
RESULTS = []


class Search:
    """Functions that allow user to search for host or service"""

    def search_host(self, search_term_host):
        matches.clear()
        print(f'Searching for {search_term_host}')
        for nag, key in nagiosKeys.items():
            nagios_data = requests.get(
                generate_url_hosts(nag, search_term_host, key)).json()
            hosts_count = nagios_data['recordcount']
            if int(hosts_count) == 0:
                pass
            elif type(nagios_data['hoststatus']) == list:
                for host in nagios_data['hoststatus']:
                    if 'host_name' in host:
                        matches.append({
                            "Host": host['host_name'],
                            "Monitored": "Yes",
                            "Environment": nag
                        })
                    elif 'name' in host:
                        matches.append({
                            "Host": host['name'],
                            "Monitored": "Yes",
                            "Environment": nag
                        })
            else:
                matches.append({
                    "Host": nagios_data['hoststatus']['display_name'],
                    "Environment": nag
                })

    def search_service(self, search_term_service):
        matches.clear()
        print(f'Searching for {search_term_service}')
        for nag, key in nagiosKeys.items():
            nagios_data = requests.get(
                generate_url_services(nag, search_term_service, key)).json()
            service_count = nagios_data['recordcount']
            if int(service_count) == 0:
                pass
            elif type(nagios_data['servicestatus']) == list:
                for service in nagios_data['servicestatus']:
                    matches.append({
                        "Host": service['host_name'],
                        "Service": service['display_name'],
                        "Environment": nag
                    })
            else:
                matches.append({
                    "Host": nagios_data['servicestatus']['host_name'],
                    "Service": nagios_data['servicestatus']['name'],
                    "Environment": nag
                })
        print(matches)

    def search_file(self, search_term_host):
        print(f'Searching for {search_term_host}')
        match_count = 0
        for nag, key in nagiosKeys.items():
            nagios_data = requests.get(
                generate_url_hosts(nag, search_term_host, key)).json()
            hosts_count = nagios_data['recordcount']
            '''
            When more than one result is found, Nagios API returns a list.
            '''
            if int(hosts_count) == 0:
                pass
            elif type(nagios_data['hoststatus']) == list:
                # Get the initial results
                for host in nagios_data['hoststatus']:
                    # Search through  the initial matches for exact matches
                    if 'host_name' in host:
                        print(host)
                        if search_term_host.lower() in host['host_name'].lower():
                            RESULTS.append({
                                "Host": host['host_name'],
                                "Monitored": "Yes",
                                "Environment": nag
                            })
                    elif 'name' in host:
                        print(host)
                        if search_term_host.lower() in host['name'].lower():
                            RESULTS.append({
                                "Host": host['name'],
                                "Monitored": "Yes",
                                "Environment": nag
                            })
                match_count += 1
            else:
                '''
                When just 1 result is found, Nagios API returns a dictionary.
                '''
                RESULTS.append({
                    "Host": nagios_data['hoststatus']['display_name'],
                    "Monitored": "Yes",
                    "Environment": nag
                })
                match_count += 1

        if match_count == 0:
            RESULTS.append({
                "Host": search_term_host,
                "Monitored": 'No'
            })
        else:
            pass
