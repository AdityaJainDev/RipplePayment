
from firebase import Firebase
import time

config = {
    "apiKey": "AIzaSyBAhBktobrVeyAvkYC86CsbpU--SUpyI3Y",
    "authDomain": "crypto-5e295.firebaseapp.com",
    "databaseURL": "https://crypto-5e295-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "crypto-5e295",
    "storageBucket": "crypto-5e295.appspot.com",
    "messagingSenderId": "607647446173",
    "appId": "1:607647446173:web:aade30f7ad9bbd9e5b5074"
}

firebase = Firebase(config)
auth = firebase.auth()
db = firebase.database()
	
while True:
	try:
		if (db.child("users").get().val()["amount"]):
			print(db.child("users").get().val()["address"])
	except:
		time.sleep(1)
					


