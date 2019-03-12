from dotenv import load_dotenv
load_dotenv()
import os
RABBITHOST = os.getenv('RABBIT_HOST')
RABBITPORT = os.getenv("RABBIT_PORT")

RABBITUSERNAME = os.getenv("RABBIT_USERNAME")
RABBITPASS = os.getenv("RABBIT_PASS")

MONGOHOST = os.getenv('MONGO_HOST')
MONGOPORT = os.getenv('MONGO_PORT')
