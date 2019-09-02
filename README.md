# gs2fb-public (python 2.7)

Upload data from google sheets tables to firebase realtime database 

# Requirements
- a google account with google sheets api enabled (https://developers.google.com/sheets/api/)
- a google sheet, with permission to access given to your google account
- firebase realtime database

# Data format

All data in whatever sheet is named "Sheet1" (the default sheet name) gets uploaded.

One column should be named "id" and contain a number.  This will be used as the key representing that row of data in firebase.  This value is saved as an integer in firebase, while everything else is saved as a string.

Google sheet data should be in the following format:

```
| id | Header 1 | Header 2 | Header 3 |
| 1  | Data 1,1 | Data 2,1 | Data 3,1 |
| 2  | Data 1,2 | Data 2,2 | Data 3,2 |
```

The data will be saved to firebase in the following (son equivalent) format:

```
{ 
	"tablename" : { 
		"1" : {
			"id" : 1
			"Header 1" : "Data 1,1"
			"Header 2" : "Data 2,1"
			"Header 3" : "Data 3,1"
		},
		"2" : {
			"id" : 2
			"Header 1" : "Data 1,2"
			"Header 2" : "Data 2,2"
			"Header 3" : "Data 3,2"
		}
	}
}
```

# Use

Install the following packages:

```
pip install pyrebase

pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

You will need three things to update a table:

- sheet ID: this can be found in the url of your google sheet.
```
sheetID = ['789hjkdslHF78907FDHJAK246HGI'] 
```
- table name: this is the name of the destination table in firebase.
```
tableName = ['my_table']
```
- DB config: this is information about your firebase database.
```
DBconfig = {
	"apiKey": "your api key",
	"authDomain": "your auth domain",
	"databaseURL": "your db url",
	"storageBucket": "your storage bucket"
}
```

Then, with gs2fb.py in your directory, import updateTable:

```
from gs2fb import updateTable
```
And call it to update a table:

```
updateTable(tableName, sheetID, DBconfig)
```



