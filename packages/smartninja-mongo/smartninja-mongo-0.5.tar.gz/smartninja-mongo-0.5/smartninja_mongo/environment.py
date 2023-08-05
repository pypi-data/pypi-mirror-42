import os


def is_mongo_env():
    # if Heroku (DYNO), Azure (APPSETTING_WEBSITE_SITE_NAME) or custom env variable (CUSTOM_MONGO_SERVER)
    if os.environ.get("DYNO") or os.environ.get("APPSETTING_WEBSITE_SITE_NAME") or os.environ.get("CUSTOM_MONGO_SERVER"):
        return True
    else:  # TinyDB on localhost
        return False
