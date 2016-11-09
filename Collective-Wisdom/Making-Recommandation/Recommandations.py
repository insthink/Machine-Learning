# coding: UTF-8
from math import sqrt

class Recommandations(object):
    def __init__(self, origin_data):
        self.od = origin_data

    # 将原数据集变为基于物品的
    def transformod(self):
        items = list(set([item for p in self.od for item in self.od[p]]))

        trans = {}
        for item in items:
            persons = {p: self.od[p][it] for p in self.od for it in self.od[p]}
            trans[item] = persons
        self.od = trans

    # 计算两人的欧式距离来判断相似度
    def calSimilarity(self, person1, person2):
        # 判断比较的两人是否在数据集里面
        if person1 not in self.od or person2 not in self.od:
            print "person not in the list"
        # 两人的共同物品
        common = [item for item in self.od[person1] if item in self.od[person2]]
        if not common:
            return False
        # 计算欧式距离
        item_distance = [
            pow(self.od[person1][item] - self.od[person2][item], 2)
            for item in common]

        return 1 / (1 + sqrt(sum(item_distance)))

    # 计算两人的皮尔逊相关系数
    def calPearson(self, person1, person2):
        # 判断比较的两人是否在数据集里面
        if person1 not in self.od or person2 not in self.od:
            print "person not in the list"
        # 两人的共同物品
        common = [item for item in self.od[person1] if item in self.od[person2]]
        n  = len(common)
        if not common:
            return False
        # 计算X,Y各自期望,等概率分布
        sum1 = sum([self.od[person1][item] for item in common])
        sum2 = sum([self.od[person2][item] for item in common])
        Ex, Ey = sum1 / n, sum2 / n

        # 计算X^2,Y^2各自期望
        sum1sq = sum([pow(self.od[person1][item], 2) for item in common])
        sum2sq = sum([pow(self.od[person2][item], 2) for item in common])
        Ex2, Ey2 = sum1sq / n, sum2sq / n

        # 计算X*Y的期望
        cross_sum = sum([self.od[person1][item] * self.od[person2][item] for item in common])
        Exy = cross_sum / n

        # 计算相关系数
        top = Exy - Ex * Ey
        bottom = sqrt((Ex2 - pow(Ex, 2)) * (Ey2 - pow(Ey, 2)))
        if bottom == 0: return 0
        return top / bottom

    # 在已知数据中寻找与自己品位最相近的topN
    def topN(self, person, n, similarity = calPearson):
        scores = [(p, similarity(person, p)) for p in self.od if p != person]
        scores.sort(key=lambda s:s[1], reverse=True)

        return scores[:n]


    def recommandIt(self, person, similarity = calPearson):
        totals = {}
        sim_sum = {}
        for p in self.od:
            if p == person: continue
            sim = similarity(person, p)

            if sim <= 0: continue
            for item in self.od[p]:
                if item not in self.od[person] or self.od[person][item] == 0:
                    totals.setdefault(item, 0)
                    totals[item] += self.od[p][item] * sim
                    sim_sum.setdefault(item, 0)
                    sim_sum[item] += sim

        rankings = [(item, total/sim_sum[item]) for item, total in totals.iteritems()]
        rankings.sort(key=lambda s:s[1], reverse=True)
        return rankings




if __name__ == "__main__":
    critics = {
        'Lisa Rose': {
            'Lady in the Water': 2.5,
            'Snakes on a Plane': 3.5,
            'Just My Luck': 3.0,
            'Superman Returns': 3.5,
            'You, Me and Dupree': 2.5,
            'The Night Listener': 3.0,
        },
        'Gene Seymour': {
            'Lady in the Water': 3.0,
            'Snakes on a Plane': 3.5,
            'Just My Luck': 1.5,
            'Superman Returns': 5.0,
            'You, Me and Dupree': 3.0,
            'The Night Listener': 3.5,
        },
        'Micheal Phillips': {
            'Lady in the Water': 2.5,
            'Snakes on a Plane': 3.0,
            'Just My Luck': 3.5,
            'The Night Listener': 4.0,
        },
        'Claudia Puid': {
            'Snakes on a Plane': 3.5,
            'Just My Luck': 3.0,
            'Superman Returns': 4.0,
            'The Night Listener': 4.5,
        },
        'Mick Lasalle': {
            'Lady in the Water': 3.0,
            'Snakes on a Plane': 4.0,
            'Just My Luck': 2.0,
            'Superman Returns': 3.0,
            'You, Me and Dupree': 3.5,
        },
        'Jack Matthews': {
            'Lady in the Water': 3.0,
            'Snakes on a Plane': 4.0,
            'Just My Luck': 2.0,
            'Superman Returns': 5.0,
            'You, Me and Dupree': 3.5,
            'The Night Listener': 3.0,
        },
        'Toby': {
            'Snakes on a Plane': 4.5,
            'Superman Returns': 4.0,
            'You, Me and Dupree': 1.0,
        },
    }
    r = Recommandations(critics)
    top_n = r.topN('Toby', 4, similarity=r.calPearson)
    rank = r.recommandIt('Toby', similarity=r.calPearson)
    print "------------------"
    print r.od
    r.transformod()
    print r.od

