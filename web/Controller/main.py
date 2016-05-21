x = """
{
    "statuses": [
        {
            "created_at": "Tue May 31 17:46:55 +0800 2011"
            }]

}

"""
import json
import datetime
y = json.loads(x)
print(y["statuses"][0]['created_at'])
z = datetime.datetime.strptime('Tue May 31 17:46:55 +0900 2011', '%a %b %d %H:%M:%S %z %Y')
print(z.minute)