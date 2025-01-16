import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dfskfsdjlf23jhtlkgjsdlkgjl'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'app/static/uploads/photos'
    WEEKLY_FOLDER = os.environ.get('WEEKLY_FOLDER') or 'app/static/uploads/weekly'
    TOKEN = os.environ.get('TOKEN') or '7792011510:AAHK_rKdfaMHKWQX9o7DW8jVsqxFnGToYQU___'
    GROUP_ID = os.environ.get('GROUP_ID') or '-4614020839'
    API_VERSION = os.environ.get('API_VERSION') or 'v1'