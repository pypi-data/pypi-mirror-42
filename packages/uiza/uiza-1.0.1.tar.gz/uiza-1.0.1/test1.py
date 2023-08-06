# from uiza.entity.entity import Entity
# from uiza.base.connections import Connection
# from uiza import Connection
from uiza import Connection
from uiza.api_resources.entity import Entity
from uiza.api_resources.user import User
from uiza.api_resources.category import Category
from uiza.api_resources.storage import Storage
from uiza.api_resources.livestreaming import LiveStreaming
from uiza.api_resources.callback import Callback
from uiza.api_resources.analytic import Analytic

if __name__ == '__main__':
    user_data = {
        # "id": "9f1cd871-9244-48a1-a233-846a3b540741",
        "status": 1,
        "username": "test_admin_pythonvnn 1",
        "email": "user_test@uiza.io",
        "fullname": "User Test",
        "avatar": "https://exemple.com/avatar.jpeg",
        "dob": "05/15/2018",
        "gender": 0,
        "password": "FMpsr<4[dGPu?B#u",
        "isAdmin": 1
    }

    data_pw = {
        'id': "9f1cd871-9244-48a1-a233-846a3b540741",
        "oldPassword": "S57Eb{:aMZhW=)G$",
        "newPassword": "FMpsr<4[dGPu?B#u"
    }

    workspace_api_domain = 'apiwrapper.uiza.co'
    api_key = 'uap-a2aaa7b2aea746ec89e67ad2f8f9ebbf-fdf5bdca'

    connection = Connection(workspace_api_domain=workspace_api_domain, api_key=api_key)
    # x, _ = User(connection).create(**user_data)
    # x = user.update(**data)
    # x = user.update_password(**data_pw)
    # x = user.delete('ddf09dd0-b7a8-4f29-92df-14dafb97b2aa')
    # x, _ = User(connection).logout()
    # x = user.get_list()
    # x, _ = User(connection).retrieve('46376b2a-9dce-4638-8afa-dab0eaadd95c')

    entity_data = {
        "name": "Sample Video Python 3",
        "url": "https://example.com/video.mp4",
        "inputType": "http",
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry'\''s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
        "shortDescription": "Lorem Ipsum is simply dummy text of the printing and typesetting industry",
        "poster": "https://example.com/picture001.jpeg",
        "thumbnail": "https://example.com/picture002.jpeg",
        "extendMetadata": {
            "movie_category": "action",
            "imdb_score": 8.8,
            "published_year": "2018"
        },
        "embedMetadata": {
            "artist": "John Doe",
            "album": "Album sample",
            "genre": "Pop"
        },
        "metadataIds": ["16a9e425-efb0-4360-bd92-8d49da111e88"]
    }

    # entity_data_update = {
    #     "name": "Title edited",
    #     "description": "Description edited",
    #     "shortDescription":"001 Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
    #     "poster":"/example.com/picture001a",
    #     "thumbnail":"/example.com/picture001a",
    #     "extendMetadata":{
    #         "movie_category":"action",
    #         "imdb_score":8.8,
    #         "published_year":"2018"
    #     }
    # }
    #

    entity = Entity(connection)
    x, _ = entity.create(**entity_data)
    # x, _ = entity.retrieve('33a86c18-f502-41a4-9c4c-d4e14efca238')
    # x, _ = entity.list()
    # x, _ = entity.update(id='id', body=entity_data_update)
    # x, _ = entity.search(keyword="Title abc")
    # x, _ = entity.publish()
    # # x, _ = entity.get_status_publish_entity(id='33a86c18-f502-41a4-9c4c-d4e14efca238')
    # x, _ = Entity(connection).get_aws_upload_key()


    # print(x)
    category = Category(connection)
    category_data = {
        # "id": "29f7b6ba-e2a7-4d4b-8026-30828d0e1bb0",
        "name":"Folder sample python 6",
        "type":"tag",
        "description":"Folder description",
        "orderNumber":1,
        "icon":"https://exemple.com/icon.png"
    }
    # x, _ = category.create(**category_data)
    # x, _ = category.retrieve('29f7b6ba-e2a7-4d4b-8026-30828d0e1bb0')
    # x, _ = category.list()
    # x, _ = category.update(**category_data)
    # x, _ = category.delete('01b658df-2ed6-4332-a2ef-004480558f34')

    # category_relation_data = {
    #     "entityId": 'eb578480-6311-4534-b00e-7c7ffbce8283',
    #     "metadataIds": ["29f7b6ba-e2a7-4d4b-8026-30828d0e1bb0"]
    # }
    # x, _ = category.delete_relation(**category_relation_data)


    storage = Storage(connection)
    storage_data = {
        "id": "415db769-8b09-4da6-85e6-a944238fcc13",
        "name":"FTP Uiza test 4",
        "description":"FTP of Uiza, use for transcode",
        "storageType":"ftp",
        "host":"ftp-example.uiza.io"
    }

    # x, _ = storage.create(**storage_data)
    # x, _ = storage.retrieve('415db769-8b09-4da6-85e6-a944238fcc13')
    # x, _ = storage.update(**storage_data)
    # x, _ = storage.delete('415db769-8b09-4da6-85e6-a944238fcc13')
    # x, _ = storage.list()


    live = LiveStreaming(connection)
    live_data = {
        "name":"test event python 1",
        "mode":"push",
        "encode":1,
        "dvr":1,
        "description":"This is for test event",
        "poster":"//image1.jpeg",
        "thumbnail":"//image1.jpeg",
        "linkStream":[
                  "https://playlist.m3u8"
                ],
        "resourceMode":"single"
    }
    update_live_data = {
        "id":"90130ea3-8898-4459-9cbf-dc335591d587",
        "name":"live test",
        "mode":"pull",
        "encode":0,
        "dvr":1,
        "resourceMode":"single"
    }

    # x, _ = live.create(**live_data)
    # x, _ = live.retrieve('90130ea3-8898-4459-9cbf-dc335591d587')
    # x, _ = live.update(**update_live_data)
    # x, _ = live.start_feed('90130ea3-8898-4459-9cbf-dc335591d587')
    # x, _ = live.stop_feed('90130ea3-8898-4459-9cbf-dc335591d587')
    # '90130ea3-8898-4459-9cbf-dc335591d587'
    # x, _ = live.get_view_feed('90130ea3-8898-4459-9cbf-dc335591d587')
    # x, _ = live.list_recorded()
    # x, _ = live.convert_into_vod()


    callback = Callback(connection)
    callback_data = {
        "id": "3cc78b68-f412-4298-80b8-8a382893e3ce",
        "url":"https://callback-url-python.uiza.co",
        "method":"GET"
    }

    # x, _ = callback.create(**callback_data)
    # x, _ = callback.retrieve('3cc78b68-f412-4298-80b8-8a382893e3ce')
    # x, _ = callback.update(**callback_data)
    # x, _ = callback.delete('3cc78b68-f412-4298-80b8-8a382893e3ce')


    analytic = Analytic(connection)
    # x, _ = analytic.get_total_line(
    #     start_date='2018-11-01 20:00',
    #     end_date='2019-11-02 20:00',
    #     metric='rebuffer_count'
    # )

    # x, _ = analytic.get_type(
    #     start_date='2018-11-01 20:00',
    #     end_date='2019-11-02 20:00',
    #     type_filter='country'
    # )


    # x, _ = analytic.get_line(
    #     start_date='2018-11-01 20:00',
    #     end_date='2019-11-02 20:00',
    # )
    print(_)
    print(x.id)

