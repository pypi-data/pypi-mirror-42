import os

from cloudshell.recorder.bootstrap import new
from cloudshell.recorder.recorder_orchestrator import RecorderOrchestrator

if __name__ == "__main__":
    import datetime

    # current = datetime.datetime.utcnow()
    # # ip = "10.215.12.6"
    # # ip = "192.168.73.66"
    # ip = "192.168.105.11"
    # # ip = "192.168.42.235"
    # # ip = "192.168.42.169"
    # # snmp_user = "quali_user"
    # snmp_user = "snmp_user_v3"
    # # snmp_pass = "quali_pass"
    # snmp_pass = "Password1"
    # # snmp_priv = "quali_priv"
    # snmp_priv = "Password2"
    # # auth_protocol = "SHA"
    # auth_protocol = "SHA"
    # # priv_protocol = "AES128"
    # priv_protocol = "DES"
    # destination_path = "%APPDATA%\\Quali\\Recordings"
    # obj = RecorderOrchestrator(ip, recording_type="all", destination_path=destination_path)
    # # obj.new_recording(snmp_user=snmp_user, snmp_password=snmp_pass, snmp_private_key=snmp_priv,
    # #                   snmp_auth_protocol=auth_protocol, snmp_priv_protocol=priv_protocol, snmp_bulk=True)
    # obj.new_recording(snmp_community="public", snmp_bulk=True)
    # # with open(os.path.expandvars("{0}\\192.168.105.11.snmp.new.bulk".format(destination_path, ip))) as file:
    # #     file_list = file.read().split("\n")
    # #     if len(file_list) == len(set(file_list)):
    # #         print "success"
    # #     else:
    # #         print "failed: len of the list - {}, len of uniqe lines - {}".format(len(file_list), len(set(file_list)))
    #
    # print "finished in" + str(datetime.datetime.utcnow() - current)

