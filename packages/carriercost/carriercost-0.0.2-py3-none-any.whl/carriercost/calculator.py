import math
import addlib
from .reader import CPFReader, TableReader
from copy import deepcopy


class Package(object):

    def __init__(self):
        self.length = 0
        self.width = 0
        self.height = 0
        self.weight = 0
        self.dep_province = ""
        self.dep_city = ""
        self.dep_district = ""
        self.des_province = ""
        self.des_city = ""
        self.des_district = ""

    def set_box(self, length, width, height, weight):
        assert length >= 0 and width >= 0 and height >= 0 and weight >= 0, "input must be nonnegative!"
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight

    def set_departure(self, dep_province=None, dep_city=None, dep_district=None):
        dep = addlib.parse_address(dep_province, dep_city, dep_district)
        self.dep_province = dep[0]
        self.dep_city = dep[1]
        self.dep_district = dep[2]

    def set_destination(self, des_province=None, des_city=None, des_district=None):
        des = addlib.parse_address(des_province, des_city, des_district)
        self.des_province = des[0]
        self.des_city = des[1]
        self.des_district = des[2]

    @property
    def volume(self):
        return self.length * self.width * self.height


class CostCalculator(object):

    def __init__(self, file_cpf, file_table):
        self.global_params = CPFReader(file_cpf).params
        self.price_table = TableReader(file_table)

    def __get_params(self, package):
        params = deepcopy(self.global_params)
        price = self.price_table.get_price(package.dep_province, package.dep_city, package.dep_district,
                                           package.des_province, package.des_city, package.des_district)
        if not price:
            return {}
        for key in price.keys():
            if key not in params.keys():
                raise ValueError("incorrect parameter name: %s" % key)
            else:
                params[key] = price[key]
        return params

    @staticmethod
    def __round(x, method):
        """ 正整数的取整的方式.

        :param x: 小数或者整数
        :param method: 0 -- 不取整; 1 -- 向上取整; -1 -- 向下取整; 2 -- 按0.5向上取整; 3 -- 四舍五入
        :return: 整数.
        """
        assert method in (0, 1, -1, 2, 3), "method takes integer values in (0, 1, -1, 2, 3)!"
        assert x >= 0, "input must be nonnegative!"

        if method == 0:
            return x
        if method == 1:
            return math.ceil(x)
        if method == -1:
            return math.floor(x)
        if method == 2:
            if x > math.floor(x) + 0.5:
                return math.ceil(x)
            elif x > math.floor(x):
                return math.floor(x) + 0.5
            else:
                return x
        if method == 3:
            return round(x)

    def get_cost(self, package):
        params = self.__get_params(package)
        volume_weight = package.volume / params['volWeightParam']
        charge_weight = self.__round(max(package.weight, volume_weight), method=params['weightRoundMeth'])
        std_cost = params['startPrice'] + max(charge_weight - params['startWeight'], 0) * params['afterPrice']
        std_cost_rounded = self.__round(std_cost, method=params['costRoundMeth'])
        cost = min(max(std_cost_rounded, params['minCost']), params['maxCost'])
        if (params['minWeight'] <= package.weight <= params['maxWeight'] and
                params['minLength'] <= max(package.length, package.width, package.height) <= params['maxLength'] and
                params['minVolume'] <= package.volume <= params['maxVolume']):
            return cost
        else:
            return 0
