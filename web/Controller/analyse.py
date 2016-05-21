from web import app
from web.Model.database import My,Public
from collections import Counter
import jieba
@app.route('/anayse')
def anayse():
    datas = Public.query.all()
    total = Counter()
    for one in datas:
        seg_list = jieba.cut(one.text, cut_all=False)
        one.cipin = Counter(seg_list)
        total.update(one.cipin)
        # print(one.cipin)
    print('------')
    print(total.most_common())
    return 'ddd'