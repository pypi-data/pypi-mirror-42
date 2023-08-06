import pkg_resources


def supported_protocols():

    protocols = []
    for d in pkg_resources.working_set:
        print(d)
        for protocol in pkg_resources.get_entry_map(d.project_name, 'fs.opener'):
            print(protocol)
            protocols.append(protocol)
    return protocols


print(supported_protocols())

import fs.opener.registry
print(fs.registry.protocols)
