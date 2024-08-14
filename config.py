#Secret key
SECRET_KEY = 'eOio8fxpALTDRf-hxHpA_cs7ekewX0MBM5c2JeGfClo'
SECURITY_PASSWORD_SALT = '109736161404603884828353211322546822202'

# Database Configuration
SQLALCHEMY_DATABASE_URI = 'postgresql://captain: @localhost:5432/sms'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True,}

# Registration
SECURITY_REGISTERABLE = True
SECURITY_CONFIRMABLE = True

#Recover/reset
SECURITY_RECOVERABLE = True

# Cookie settings
REMEMBER_COOKIE_SAMESITE = 'strict' #server side
SESSION_COOKIE_SAMESITE = 'strict' # client side


# Configuration for Gmail's SMTP server
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'enockbett427@gmail.com' 
MAIL_PASSWORD = 'ypsh pumk lluj hkeu'     
MAIL_USE_TLS = True
MAIL_DEFAULT_SENDER = 'enockbett427@gmail.com'

SECURITY_CHANGE_EMAIL = True
