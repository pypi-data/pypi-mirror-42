import os

destination_path = "%APPDATA%\\Quali\\Recordings"
success = False
with open(os.path.expandvars("{0}\\192.168.105.11.snmp".format(destination_path))) as file:
    file_list_walk = file.read().split("\n")
    with open(os.path.expandvars("{0}\\192.168.105.11.snmp.bulk".format(destination_path))) as file:
        file_list_bulk = file.read().split("\n")
        for item in file_list_walk:
            success = False
            walk_item = item.split(",")[0]
            for item2 in file_list_bulk:
                bulk_item = item2.split(",")[0]
                if bulk_item == walk_item:
                    success = True
                    break
            if not success:
                print item