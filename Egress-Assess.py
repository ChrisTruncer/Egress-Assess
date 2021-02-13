#!/usr/bin/python3

# This tool is designed to be an easy way to test exfiltrating data
# from the network you are currently plugged into.  Used for red or
# blue teams that want to test network boundary egress detection
# capabilities.


import logging
import sys
from common import helpers
from common import orchestra

if __name__ == "__main__":

    logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

    helpers.title_screen()

    cli_parsed = helpers.cli_parser()

    the_conductor = orchestra.Conductor()

    # Check if only listing supported server/client protocols or datatypes
    if cli_parsed.list_servers:
        print('[*] Supported server protocols: \n')
        the_conductor.load_server_protocols(cli_parsed)
        for name, server_module in sorted(the_conductor.server_protocols.items()):
            print(f'[+] {server_module.protocol}')
        sys.exit()

    elif cli_parsed.list_clients:
        print('[*] Supported client protocols: \n')
        the_conductor.load_client_protocols(cli_parsed)
        for name, client_module in sorted(the_conductor.client_protocols.items()):
            print(f'[+] {client_module.protocol}')
        sys.exit()

    elif cli_parsed.list_datatypes:
        print('[*] Supported data types: \n')
        the_conductor.load_datatypes(cli_parsed)
        for name, datatype_module in sorted(the_conductor.datatypes.items()):
            print(f'[+] {datatype_module.cli}' + " - (" +
                  datatype_module.description + ")")
        sys.exit()

    elif cli_parsed.list_actors:
        print('[*] Supported malware/APT groups: \n')
        the_conductor.load_actors(cli_parsed)
        for name, datatype_module in sorted(the_conductor.actor_modules.items()):
            print(f'[+] {datatype_module.cli}' + " - (" +
                  datatype_module.description + ")")
        sys.exit()

    if cli_parsed.server is not None:
        the_conductor.load_server_protocols(cli_parsed)
        the_conductor.load_actors(cli_parsed)

        # Check if server module is given threat actor vs. normal server
        for actor_path, actor_mod in the_conductor.actor_modules.items():

            # If actor module is what is used, search for the server requirement
            # and load that
            if actor_mod.cli == cli_parsed.server.lower():

                for full_path, server_actor in the_conductor.server_protocols.items():

                    if server_actor.protocol.lower() == actor_mod.server_requirement:
                        server_actor.serve()

        for full_path, server in the_conductor.server_protocols.items():

            if server.protocol == cli_parsed.server.lower():
                server.serve()

    elif cli_parsed.client is not None:
        # load up all supported client protocols and datatypes
        the_conductor.load_client_protocols(cli_parsed)
        the_conductor.load_datatypes(cli_parsed)

        if cli_parsed.file is None:
            # Loop through and find the requested datatype
            for name, datatype_module in the_conductor.datatypes.items():
                if datatype_module.cli == cli_parsed.datatype.lower():
                    generated_data = datatype_module.generate_data()

                    # Once data has been generated, transmit it using the
                    # protocol requested by the user
                    for proto_name, proto_module in the_conductor.client_protocols.items():
                        if proto_module.protocol == cli_parsed.client.lower():
                            proto_module.transmit(generated_data)
                            sys.exit()

        else:
            with open(cli_parsed.file, 'rb') as file_data_handle:
                file_data = file_data_handle.read()

            for proto_name, proto_module in the_conductor.client_protocols.items():
                if proto_module.protocol == cli_parsed.client.lower():
                    proto_module.transmit(file_data)
                    sys.exit()

        print("[*] Error: You either didn't provide a valid datatype or client protocol to use.")
        print('[*] Error: Re-run and use --list-datatypes or --list-clients to see possible options.')
        sys.exit()

    elif cli_parsed.actor is not None:
        # Load different threat actors/malware
        the_conductor.load_actors(cli_parsed)

        # Identify the actor to emulate
        for full_path, actor_variant in the_conductor.actor_modules.items():
            if actor_variant.cli == cli_parsed.actor.lower():

                # Check if generating data or using data within the actor module
                if cli_parsed.datatype is not None:
                    the_conductor.load_datatypes(cli_parsed)

                    # Generate the data for the actor to exfil
                    for name, datatype_module in the_conductor.datatypes.items():
                        if datatype_module.cli == cli_parsed.datatype.lower():
                            generated_data = datatype_module.generate_data()

                    actor_variant.emulate(data_to_exfil=generated_data)

                # Instead, use the exfil data within the module
                else:
                    actor_variant.emulate()
