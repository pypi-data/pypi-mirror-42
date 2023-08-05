import json
import addlib


class CPFReader(object):

    """ 读CPF配置.
    """

    INF = 10000000

    def __init__(self, file):
        self.__file = file
        self.params = {}
        self.__init()

    def __init(self):
        with open(self.__file, encoding='utf-8') as f:
            for line in f.readlines():
                kv = line.split('#', 1)[0].split('=', 1)
                if len(kv) != 2:
                    continue
                k, v = kv[0].strip(), kv[1].strip()
                if v == "INF":
                    v = self.INF
                elif v.isnumeric():
                    v = int(v)
                else:
                    v = float(v)
                self.params[k] = v


class TableReader(object):
    """ 读定价表.
    """

    def __init__(self, file):
        self.__file = file
        self.__table = {}
        self.__init()

    def __init(self):
        with open(self.__file, encoding='utf-8') as f:
            for line in f.readlines():
                row = line[0: -1].split('\t')
                dep_province = row[0] if row[0] != "NULL" else ""
                dep_city = row[1] if row[1] != "NULL" else ""
                dep_district = row[2] if row[2] != "NULL" else ""
                des_province = row[3] if row[3] != "NULL" else ""
                des_city = row[4] if row[4] != "NULL" else ""
                des_district = row[5] if row[5] != "NULL" else ""
                price = json.loads(row[6])
                key = self.__format_key(dep_province, dep_city, dep_district,
                                        des_province, des_city, des_district)
                if not key:
                    raise ValueError("Error in: %s-%s-%s-%s-%s-%s" % (dep_province, dep_city, dep_district,
                                     des_province, des_city, des_district))
                self.__table[key] = price

    @staticmethod
    def __format_key(dep_province, dep_city, dep_district,
                     des_province, des_city, des_district):
        dep = addlib.parse_address(dep_province, dep_city, dep_district)
        des = addlib.parse_address(des_province, des_city, des_district)
        return "".join(dep) + "".join(des)

    @staticmethod
    def __get_query_keys(dep_province, dep_city, dep_district,
                         des_province, des_city, des_district):
        """ 获取查询的索引关键字.
            按区, 市, 省的级别由小到大进行查询.
        """
        dep = addlib.parse_address(dep_province, dep_city, dep_district)
        des = addlib.parse_address(des_province, des_city, des_district)
        level = 3
        for i in range(level):
            if dep[level - i - 1]:
                dep = dep[0:level - i]
                break
        for i in range(level):
            if des[level - i - 1]:
                des = des[0:level - i]
                break
        dep_size = len(dep)
        des_size = len(des)

        keys = []
        for i in range(dep_size):
            dep_temp = dep[0: dep_size - i]
            for j in range(des_size):
                des_temp = des[0: des_size - j]
                keys.append("".join(dep_temp) + "".join(des_temp))
        return keys

    def get_price(self, dep_province=None, dep_city=None, dep_district=None,
                  des_province=None, des_city=None, des_district=None):

        query_keys = self.__get_query_keys(dep_province, dep_city, dep_district,
                                           des_province, des_city, des_district)
        for k in query_keys:
            if k in self.__table.keys():
                return self.__table[k]

        return None
