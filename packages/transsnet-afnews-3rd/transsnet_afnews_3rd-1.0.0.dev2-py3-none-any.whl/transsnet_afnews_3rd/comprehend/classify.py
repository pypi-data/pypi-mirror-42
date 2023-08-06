import re
import time
import pymongo
from transsnet_afnews_3rd.comprehend import s3driver

BATCH_SIZE = 1000
client = pymongo.MongoClient(host='172.31.64.135', port=3119, username='', password='')
print(client)
database = client.get_database('crawler')
database.authenticate(name='appuser', password='jk_jf4JjHf_048')
collection = database.get_collection("news_history")

count = collection.count()
print('total documents count = %s' % count)

time = time.time()
filename = 'tmp' + time
tmp_file = './'+filename
with open(tmp_file, 'a') as tmp:
    cur_count = 0
    while cur_count < count:
        for document in collection.find().sort([('_id', pymongo.DESCENDING)]).limit(BATCH_SIZE).skip(cur_count):
            content_text = str(document['content_text'])
            content = re.sub('\s', ' ', content_text)
            category = document['categories'][0]
            tmp.write(content)
            tmp.write('\n')
            tmp.flush()
        cur_count += BATCH_SIZE
print('finished')

s3driver.upload_file_to_s3(filename=filename)
print('upload file to s3')

