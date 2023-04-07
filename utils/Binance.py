from conf import client


def status():
    import sys

    status_code = client.get_system_status()['status']
    if status_code != 0:
        print("Exiting")
        sys.exit(1)
