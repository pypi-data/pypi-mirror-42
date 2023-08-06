import uiza
from uiza.api_resources.user import User

if __name__ == '__main__':
    uiza.workspace_api_domain = 'apiwrapper.uiza.co'
    uiza.api_key = 'uap-a2aaa7b2aea746ec89e67ad2f8f9ebbf-fdf5bdca'

    user_data = {
        "status": 1,
        "username": "test_admin_pythonvnn 6",
        "email": "user_test@uiza.io",
        "fullname": "User Test",
        "avatar": "https://exemple.com/avatar.jpeg",
        "dob": "05/15/2018",
        "gender": 0,
        "password": "FMpsr<4[dGPu?B#u",
        "isAdmin": 1
    }
    x, _ = User().create(**user_data)
    print(x.id)