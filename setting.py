from dotenv import load_dotenv
load_dotenv()
import os
RABBITHOST = os.getenv('RABBIT_HOST')
RABBITPORT = os.getenv("RABBIT_PORT")

RABBITUSERNAME = os.getenv("RABBIT_USERNAME")
RABBITPASS = os.getenv("RABBIT_PASS")

MONGOHOST = os.getenv('MONGO_HOST')
MONGOPORT = os.getenv('MONGO_PORT')

BNCAPIK= os.getenv("BINANCE_API")
BNCSECK= os.getenv("BINANCE_SEC")

REPORT_ADDR= os.getenv("REPORT_VOL_ADDR")