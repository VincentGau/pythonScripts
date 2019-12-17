import re
import time

import psycopg2

from src import local_settings


def get_hot_works():
    """
    获取作品热表
    :return:
    """
    conn = psycopg2.connect(database="postgres", user="postgres", password=local_settings.POSTGRE_PWD, host="localhost",
                            port="5432")
    c = conn.cursor()
    c.execute("select content from works where workid in (select workid from hot_works)")
    result = []
    for work in c.fetchall():
        result.append(work[0])
    return result


def keywords_filter(works, keyword):
    """
    筛选出works中包含有keyword的作品，keyword包含多个字符时只要work中有其中任意字符即为符合条件；
    :param works:
    :param keyword:
    :return:
    """
    return [work for work in works if set(work) & set(keyword)]


def get_paragraphs(work):
    """
    根据换行符将work切分成段落列表；

    注：对诗来说有用，一般情况下诗一段两联，但是对词、文等其他类型则没有意义，因为一般情况下词一段为一阙，未必是两句；
    :param work:
    :return:
    """
    return re.split('\r\n|\n', work)


def get_paragraphs_all(works):
    result = []
    for work in works:
        result += get_paragraphs(work)
    return result


def get_single_sentence(work):
    """
    切分单句，\r\n暂不处理，返回时再删去，Lazy原则
    :param work:
    :return:
    """
    return re.split('，|。|！|？', work)


def get_single_sentence_all(works):
    result = []
    for work in works:
        result += get_single_sentence(work)
    return result


def shefu(sentence, kw, limit=0):
    """

    :param sentence:
    :param kw:
    :param limit:
    :return:
    """
    r = []
    for s in get_single_sentence_all(keywords_filter(get_hot_works(), kw)):
        if set(s) & set(sentence) and set(s) & set(kw):
            one = re.sub(r'[\r\n]', '', s)
            if limit == 0:
                r.append(one)
            else:
                if len(one) == limit:
                    r.append(one)
    print(r)


# shefu('甫昔少年日', '府')


def shuangfei(s1, s2):
    ps = get_hot_works()
    ps = keywords_filter(ps, s1+s2)
    print(len(ps))
    for work in ps:
        # 以句号分区，不同区的两句排除出双飞规则判断范围
        sections = re.split('。', work)
        for section in sections:
            if not set(section) & set(s1) or not set(section) & set(s2):
                continue
            s = re.split('[，|！|？|]', section)
            if len(s) < 2:
                continue
            for i in range(len(s)-1):
                if set(s[i]) & set(s1) and set(s[i+1]) & set(s2):
                    print(re.sub(r'[\r\n]', '', s[i]), re.sub(r'[\r\n]', '', s[i+1]))
            # if set(s[0]) & set(s1) and set(s[1]) & set(s2):
            #     print(s[0], s[1])


shuangfei('无那尘缘容易绝', '燕子依然')