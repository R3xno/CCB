class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "7053677913"
    sudo_users = "7053677913", "1732582235", "5871216602"
    GROUP_ID = "-1002143253592"
    TOKEN = "8025760969:AAHUSHEjNIz_SHCot8JNENtrQFYolACt0mQ"
    mongo_url = "mongodb+srv://HaremDBBot:ThisIsPasswordForHaremDB@haremdb.swzjngj.mongodb.net/?retryWrites=true&w=majority"
    PHOTO_URL = ["https://telegra.ph/file/b925c3985f0f325e62e17.jpg", "https://telegra.ph/file/4211fb191383d895dab9d.jpg"]
    SUPPORT_CHAT = "CharacterCollectors"
    UPDATE_CHAT = "CharactersCollectionNews"
    BOT_USERNAME = "Characters_Collection_Bot"
    CHARA_CHANNEL_ID = " -1002459191712"
    api_id = 28735016
    api_hash = "395761ed41e18de91ee4e18ff99afc81"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
