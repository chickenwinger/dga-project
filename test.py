from dga.firebaseConfig import firebase

db = firebase.database()

ref = db.child('records').child('5lfaC7Q1nwXDjG4Y95eqIFs2gcb2')

print(ref.child('record 1').set({'timestamp': 1234567890, 'hydrogen': 1, 'methane': 2, 'acetylene': 3, 'ethylene': 4, 'ethane': 5, 'cmonoxide': 6, 'cdioxide': 7, 'total_combustibles': 8}))