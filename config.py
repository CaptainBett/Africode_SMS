import os

#Secret key
SECRET_KEY = 'eOio8fxpALTDRf-hxHpA_cs7ekewX0MBM5c2JeGfClo'
SECURITY_PASSWORD_SALT = '109736161404603884828353211322546822202'

#vercel postgresql database
database_url = os.environ.get('DATABASE_URL', 'postgres://default:pqa8uxi1KXJB@ep-long-truth-a4uo22y9-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

SQLALCHEMY_DATABASE_URI = database_url

# Database Configuration
# SQLALCHEMY_DATABASE_URI = 'postgresql://captain:captain@localhost:5432/sms'
# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:XRMSOWRIBmembwCWXcrzCeWvgsfpOSJK@postgres.railway.internal:5432/railway'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True,}

# Registration
SECURITY_REGISTERABLE = False     #Change here if you want to enable registering users again
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
