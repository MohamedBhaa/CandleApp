from datetime import timedelta

# ENV = 'development'
# PORT = 3050
# DEBUG = True
# PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)
# SQLALCHEMY_DATABASE_URI = 'sqlite:///candle.db'
SQLALCHEMY_DATABASE_URI = 'postgresql://lgwfruiwnclcmw:3ae53c072ca19bed73f5c3378ce1a176879dbaefab18c2775b8dfc6280b57156@ec2-52-204-195-41.compute-1.amazonaws.com:5432/d3n3mpo6ce3j2a'
SQLALCHEMY_TRACK_MODIFICATIONS = False
MSEARCH_INDEX_NAME = 'msearch'
MSEARCH_BACKEND = 'whoosh'