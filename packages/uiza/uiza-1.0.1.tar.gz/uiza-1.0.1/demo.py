import uiza
from uiza.api_resources.storage import Storage

if __name__ == '__main__':
    uiza.workspace_api_domain = 'apiwrapper.uiza.co'
    uiza.api_key = 'uap-a2aaa7b2aea746ec89e67ad2f8f9ebbf-fdf5bdca'

    data = {
        "name":"FTP Uiza Test Python",
        "description":"FTP of Uiza, use for transcode",
        "storageType":"ftp",
        "host":"ftp-example.uiza.io",
        "username":"uiza",
        "password":"=59x@LPsd+w7qW",
        "port":21
    }
    # x, _ = Live().create(**data)
    x, _ = Storage().remove('0bfc33f8-30f4-46d7-b3f9-40f2a167a3bd')
    print(x.id)