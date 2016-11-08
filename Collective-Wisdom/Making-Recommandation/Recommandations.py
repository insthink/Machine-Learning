# coding: UTF-8
from math import sqrt

class Recommandations(object):
    def __init__(self, origin_data):
        self.od = origin_data
    
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
        if not common:
            return False
        # 计算总和-平方和-乘积和
        sum1 = sum([self.od[person1][item] for item in common])
        sum2 = sum([self.od[person2][item] for item in common])

        sum1sq = sum([pow(self.od[person1][item], 2) for item in common])
        sum2sq = sum([pow(self.od[person2][item], 2) for item in common])

        cross_sum = sum([self.od[person1][item] * self.od[person2][item] for item in common])
        # 计算相关系数
        



    
        

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
        'Insthink': {
            'Snakes on a Plane': 4.5,
            'Superman Returns': 4.0,
            'You, Me and Dupree': 1.0,
        }
    }
    r = Recommandations(critics)
    simi = r.calSimilarity('Toby', 'Insthink')
    print simi