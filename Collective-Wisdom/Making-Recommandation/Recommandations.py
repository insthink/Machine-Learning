# coding: UTF-8
from math import sqrt
import os.path

# 从csv文件中获得数据集
def getDataset():
    path = os.path.join(os.getcwd(), "movielens")
    movies = {}
    with open(path + "/movies.csv", "r") as f:
        for i, l in enumerate(f.xreadlines()):
            if i == 0: continue
            idx, mvname = l.split(",")[:2]
            movies[idx] = mvname

    prefs = {}
    with open(path + "/ratings.csv", "r") as f:
        for i, l in enumerate(f.xreadlines()):
            if i == 0: continue
            user, mvIdx, rating = l.split(",")[:3]
            prefs.setdefault(user, {})
            prefs[user][movies[mvIdx]] = float(rating)
    return prefs

# user-based collaboration filter
# -------------------------------
# -------------------------------

# 计算两人的欧式距离来判断相似度
def calSimilarity(od, person1, person2):
    # 判断比较的两人是否在数据集里面
    if person1 not in od or person2 not in od:
        print "person not in the list"
    # 两人的共同物品
    common = [item for item in od[person1] if item in od[person2]]
    if not common:
        return False
    # 计算欧式距离
    item_distance = [pow(od[person1][item] - od[person2][item], 2) for item in common]

    return 1 / (1 + sqrt(sum(item_distance)))

# 计算两人的皮尔逊相关系数
def calPearson(od, person1, person2):
    # 判断比较的两人是否在数据集里面
    if person1 not in od or person2 not in od:
        print "person not in the list"
    # 两人的共同物品
    common = [item for item in od[person1] if item in od[person2]]
    n  = len(common)
    if not common:
        return False
    # 计算X,Y各自期望,等概率分布
    sum1 = sum([od[person1][item] for item in common])
    sum2 = sum([od[person2][item] for item in common])
    Ex, Ey = sum1 / n, sum2 / n

    # 计算X^2,Y^2各自期望
    sum1sq = sum([pow(od[person1][item], 2) for item in common])
    sum2sq = sum([pow(od[person2][item], 2) for item in common])
    Ex2, Ey2 = sum1sq / n, sum2sq / n

    # 计算X*Y的期望
    cross_sum = sum([od[person1][item] * od[person2][item] for item in common])
    Exy = cross_sum / n

    # 计算相关系数
    top = Exy - Ex * Ey
    bottom = sqrt((Ex2 - pow(Ex, 2)) * (Ey2 - pow(Ey, 2)))
    if bottom == 0: return 0
    return top / bottom

# 在已知数据中寻找与自己品位最相近的topN
def topN(od, person, n, similarity = calPearson):
    scores = [(p, similarity(od, person, p)) for p in od if p != person]
    scores.sort(key=lambda s:s[1], reverse=True)
    return scores[:n]

# 通过相似度*评分加权来向用户推荐物品
def recommandIt(od, person, similarity = calPearson):
    totals = {}
    sim_sum = {}
    for p in od:
        if p == person: continue
        sim = similarity(person, p)

        if sim <= 0: continue
        for item in od[p]:
            if item not in od[person] or od[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += od[p][item] * sim
                sim_sum.setdefault(item, 0)
                sim_sum[item] += sim

    rankings = [(item, total/sim_sum[item]) for item, total in totals.iteritems()]
    rankings.sort(key=lambda s:s[1], reverse=True)
    return rankings

# items-based collaboration filter
# --------------------------------
# --------------------------------

# 将原数据集变为基于物品的
def transformod(od):
    result = {}
    for p in od:
        for it in od[p]:
            result.setdefault(it, {})
            result[it][p] = od[p][it]
    return result


# 构造相似度从高到低的列表
def calSimilarItems(od2, n):
    result = {}
    c = 0
    for item in od2:
        result[item] =topN(od2, item, n, calPearson)
        c += 1
        if c % 100 == 0: print "%d / %d" % (c, len(od2))
    return result

# 为用户进行推荐
def recommandItByItems(od, similarItems, user):
    user_rating = od[user]
    scores = {}
    simi = {}

    for (item, rating) in user_rating.iteritems():

        for (item2, similarity) in similarItems[item]:
            if item2 in user_rating: continue
            scores.setdefault(item2, 0)
            scores[item2] += rating * similarity

            simi.setdefault(item2, 0)
            simi[item2] += similarity

    result = [(item, score / simi[item]) for item, score in scores.iteritems()]
    result.sort(key=lambda s:s[1], reverse=True)
    return result

# homework
# ex3.
# 编写一个预先计算用户相似度的函数,为每个用户创建一个topN相似度的列表
def calSimilarPersons(od, n):
    result = {}
    c = 0
    for person in od:
        result[person] = topN(od, person, n, calPearson)
        c += 1
        if c % 100 == 0: print "%d / %d" % (c, len(od))
    return result

# 根据趣味相投的前5名用户,为用户推荐物品
def recommandItByUsers(od, user, similarPersons):
    rating_total = {}
    simi_total = 0
    for (p, simi) in similarPersons[user]:
        for (item, score) in od[p].iteritems():
            if item in od[user]: continue
            rating_total.setdefault(item, 0)
            rating_total[item] += simi * score

        simi_total += simi

    result = [(item, rating_total[item] / simi_total) for item in rating_total.keys()]
    result.sort(key=lambda s:s[1], reverse=True)
    return result




if __name__ == "__main__":
    o = getDataset()
    simiUsers = calSimilarPersons(o, 5)
    r = recommandItByUsers(o, '1', simiUsers)
    print r



# critics = {
#     'Lisa Rose': {
#         'Lady in the Water': 2.5,
#         'Snakes on a Plane': 3.5,
#         'Just My Luck': 3.0,
#         'Superman Returns': 3.5,
#         'You, Me and Dupree': 2.5,
#         'The Night Listener': 3.0,
#     },
#     'Gene Seymour': {
#         'Lady in the Water': 3.0,
#         'Snakes on a Plane': 3.5,
#         'Just My Luck': 1.5,
#         'Superman Returns': 5.0,
#         'You, Me and Dupree': 3.0,
#         'The Night Listener': 3.5,
#     },
#     'Micheal Phillips': {
#         'Lady in the Water': 2.5,
#         'Snakes on a Plane': 3.0,
#         'Just My Luck': 3.5,
#         'The Night Listener': 4.0,
#     },
#     'Claudia Puid': {
#         'Snakes on a Plane': 3.5,
#         'Just My Luck': 3.0,
#         'Superman Returns': 4.0,
#         'The Night Listener': 4.5,
#     },
#     'Mick Lasalle': {
#         'Lady in the Water': 3.0,
#         'Snakes on a Plane': 4.0,
#         'Just My Luck': 2.0,
#         'Superman Returns': 3.0,
#         'You, Me and Dupree': 3.5,
#     },
#     'Jack Matthews': {
#         'Lady in the Water': 3.0,
#         'Snakes on a Plane': 4.0,
#         'Just My Luck': 2.0,
#         'Superman Returns': 5.0,
#         'You, Me and Dupree': 3.5,
#         'The Night Listener': 3.0,
#     },
#     'Toby': {
#         'Snakes on a Plane': 4.5,
#         'Superman Returns': 4.0,
#         'You, Me and Dupree': 1.0,
#     },
# }




