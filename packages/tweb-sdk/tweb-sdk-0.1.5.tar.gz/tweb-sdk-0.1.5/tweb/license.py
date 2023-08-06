# coding:utf-8
from bitarray import bitarray
import re
from tweb.error_exception import ErrException, ERROR
from tweb import tools, rdpool, time
import os
import base64
import config


class License:
    """
    资源授权证书
    """

    def __init__(self, text=None):
        """
        :param text: 格式: "若干位0/1开关串;任意个数的数值列表;任意个数的范围列表",
        示例: 1100010010111010000100001000011100100110;12,30,100;0~100,20~50
        """

        # 开关项，在子类中具体指定
        self.SWITCH = []
        # 数值项，在子类中具体指定
        self.NUMBER = []
        # 范围项，在子类中具体指定
        self.RANGE = []

        self.authority = 'world'  # 发证机构代码，一般在子类中修改
        self.secret = 'Lic123!@#'  # 发证机构代签名密码，一般在子类中修改
        self.timeout = 604800  # 有效性超时时间, 秒
        self.idle_time = 86400  # 闲置超时时间, 秒

        # 以下字段子类不建议修改
        self.resource = None
        self.owner = None
        self.json = None
        self.text = text

    def parse(self):
        if self.text is None:
            sw_tpl_str = '0' * len(self.SWITCH)
            num_tpl_str = ','.join(['0'] * len(self.NUMBER))
            ran_tpl_str = ','.join(['0~0'] * len(self.RANGE))
            self.text = '{};{};{}'.format(sw_tpl_str, num_tpl_str, ran_tpl_str)

        if not re.match(r'[0-1]{%s};[\-0-9,]*;[\-0-9~,]*' % len(self.SWITCH), self.text):
            tpl = self.__class__().parse().text
            return ErrException(ERROR.E40000, extra='wrong format, template: %s' % tpl)

        domains = self.text.split(';')

        # 开关相关
        sw_str = domains[0]
        sw_obj = dict()
        for i, k in enumerate(self.SWITCH):
            if k == 'NA':
                continue
            if i < len(sw_str):
                sw_obj[k] = int(sw_str[i])
            else:
                sw_obj[k] = 0
        # END

        # 数值相关
        num_str = domains[1]
        nums = num_str.split(',')
        nums_len = len(nums)
        if num_str == '':
            nums_len = 0

        num_obj = dict()
        for i, k in enumerate(self.NUMBER):
            if k == 'NA':
                continue
            if i < nums_len:
                num_obj[k] = int(nums[i])
            else:
                num_obj[k] = 0
        # END

        # 范围相关
        ran_str = domains[2]
        ranges = ran_str.split(',')
        ran_len = len(ranges)
        if ran_str == '':
            ran_len = 0

        ran_obj = dict()
        for i, k in enumerate(self.RANGE):
            if k == 'NA':
                continue

            if i < ran_len:
                mm = ranges[i].split('~')
                if len(mm) != 2:
                    low = 0
                    up = 0
                else:
                    try:
                        low = int(mm[0])
                        up = int(mm[1])

                        if low > up:
                            up = low
                    except ValueError:
                        low = 0
                        up = 0

                ran_obj[k] = [low, up]
            else:
                ran_obj[k] = [0, 0]
        # END

        self.json = dict()
        if len(sw_obj) > 0:
            self.json['switch'] = sw_obj
        if len(num_obj) > 0:
            self.json['number'] = num_obj
        if len(ran_obj) > 0:
            self.json['range'] = ran_obj

        return self

    def update(self, resource, owner, json, operator_license):
        """
        :param resource: 受保护的资源标示
        :param owner: 权限授予对象
        :param json: 权限JSON描述对象, 示例如下：
                        {
                            "switch": {
                                "create": 0,
                                "read": 1,
                                ...
                            },
                            "number": {
                                "users": 100
                                ...
                            },
                            "range": {
                                "age_range": [20, 30],
                                ...
                            }
                        }
        :param operator_license:
        :return: self
        """

        if owner is None:
            owner = ''

        if owner == operator_license.owner:
            raise ErrException(ERROR.E40300, extra='can not update yourself, should be done by your parents')

        self.resource = resource
        self.owner = owner

        # 开关相关
        sw_len = len(self.SWITCH)
        sw_obj = json.get('switch')
        if sw_obj is not None and sw_len > 0:
            ba = bitarray('0' * sw_len)
            for i, k in enumerate(self.SWITCH):
                if k == 'NA':
                    continue

                # 对操作者自己被授权的本级资源授权其他主体权限时，授权不能超过自己的权限范围
                if resource == operator_license.resource:
                    if sw_obj[k]:
                        try:
                            operator_license.operable(resource, k)
                        except ErrException as e:
                            raise ErrException(ERROR.E40311, extra='exceed your own territory--%s' % e.extra)

                if k in sw_obj:
                    ba[i] = sw_obj[k]

            sw_str = ba.to01()
        else:
            sw_str = '0' * sw_len
        # END

        # 数值相关
        num_len = len(self.NUMBER)
        num_obj = json.get('number')
        if num_obj is not None and num_len > 0:
            nums = ['0'] * num_len
            for i, k in enumerate(self.NUMBER):
                if k == 'NA':
                    continue
                val = num_obj.get(k)
                if val is not None:
                    # 对操作者自己被授权的本级资源授权其他主体权限时，授权不能超过自己的权限范围
                    if resource == operator_license.resource:
                        self_limit = operator_license.number(resource, k)
                        if val > self_limit:
                            raise ErrException(ERROR.E40311, extra='exceed your own limit %s' % self_limit)

                    nums[i] = str(val)

            num_str = ','.join(nums)
        else:
            num_str = ','.join(['0'] * num_len)
        # END

        # 范围相关
        ran_len = len(self.RANGE)
        ran_obj = json.get('range')
        if ran_obj is not None and ran_len > 0:
            rans = ['0~0'] * ran_len
            for i, k in enumerate(self.RANGE):
                if k == 'NA':
                    continue
                vals = ran_obj.get(k)
                if vals is not None:
                    if len(vals) == 2:
                        # 对操作者自己被授权的本级资源授权其他主体权限时，授权不能超过自己的权限范围
                        if resource == operator_license.resource:
                            self_range = operator_license.number(resource, k)
                            if vals[0] < self_range[0] or vals[1] > self_range[1]:
                                raise ErrException(ERROR.E40311, extra='exceed your own range %s' % self_range)

                        rans[i] = '{}~{}'.format(vals[0], vals[1])

            ran_str = ','.join(rans)
        else:
            ran_str = ','.join(['0~0'] * ran_len)
        # END

        # 拼接
        text = f'{sw_str};{num_str};{ran_str}'

        # 如果新的授权串与原来不一样则更新
        if text != self.text:
            self.text = text
            self.parse()

            # 使某资源对某拥有者的授权签名全部失效
            if self.resource is not None and self.owner is not None:
                key = self._key()
                issued_list = rdpool.rds.keys(f'{key}*')
                for k in issued_list:
                    rdpool.rds.delete(k)

        return self

    def signed(self, resource, owner, nonce):
        """
        获取签名的授权字符串
        :param resource: 受保护的资源标示, 为节点node值，如'root/product'
        :param owner: 权限授予对象标示, 如组织ID，或者用户ID
        :param nonce: 临时一致性标示，如可以使用用户的access_token
        """
        if owner is None:
            owner = ''
        if nonce is None:
            nonce = ''

        self.resource = resource
        self.owner = owner
        lic_token = os.urandom(12).hex()
        key = self._key(nonce)
        rdpool.rds.set(key, lic_token, self.idle_time)

        sign = tools.gen_md5(self.text + self.resource + self.owner + nonce + lic_token)

        expired = time.second() + self.timeout

        temp = f'{self.text}&{self.resource}&{self.owner}&{sign}&{expired}'
        return str(base64.b64encode(str.encode(temp)), encoding="utf8")

    def verify(self, *auth_args):
        """
        校验授权签名的合法性
        :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
        :return: 授权对象
        """
        signed = auth_args[0]
        nonce = auth_args[1]
        if nonce is None:
            nonce = ''

        if signed is None:
            raise ErrException(ERROR.E40000, extra='no signed license')

        try:
            signed = str(base64.b64decode(signed), encoding="utf8")
        except Exception:
            raise ErrException(ERROR.E40000, extra='wrong signed license')

        fields = signed.split('&')
        if len(fields) != 5:
            raise ErrException(ERROR.E40307, extra='wrong format of signed license')

        self.text = fields[0]
        self.resource = fields[1]
        self.owner = fields[2]
        sign = fields[3]
        expired = int(fields[4])

        if time.second() > expired:
            raise ErrException(ERROR.E40310)

        key = self._key(nonce)
        lic_token = rdpool.rds.get(key)
        if lic_token is None:
            raise ErrException(ERROR.E40309)

        # 重置lic_token超时时间
        rdpool.rds.expire(key, self.idle_time)

        dynamic_sign = tools.gen_md5(self.text + self.resource + self.owner + nonce + lic_token)
        if dynamic_sign != sign:
            raise ErrException(ERROR.E40307)

        return self.parse()

    def operable(self, cur_resource, *actions):
        """
        检查是否允许进行指定操作
        :param cur_resource: 将被操作的资源路径，如'root/club/table'
        :param actions: 操作列表，如create, read...
        """
        # 判断操作目录是否是授权目录，或者授权目录的子目录
        if cur_resource.find(self.resource) != 0:
            raise ErrException(ERROR.E40306)

        for action in actions:
            if 'switch' not in self.json or action not in self.json['switch']:
                raise ErrException(ERROR.E40000, extra='wrong action of %s' % action)

            if self.json['switch'][action] == 0:
                raise ErrException(ERROR.E40308, extra=f'you can not {action}')

        return self

    def number(self, cur_resource, key):
        """
        查询授权数值
        :param cur_resource: 将被操作的资源路径，如'root/club/table'
        :param key: 字段名
        """
        # 判断操作目录是否是授权目录，或者授权目录的子目录
        if cur_resource.find(self.resource) != 0:
            raise ErrException(ERROR.E40306)

        if 'number' not in self.json or key not in self.json['number']:
            raise ErrException(ERROR.E40000, extra='wrong number key of %s' % key)

        return self.json['number'][key]

    def range(self, cur_resource, key):
        """
        查询授权的数值范围
        :param cur_resource: 将被操作的资源路径，如'root/club/table'
        :param key: 字段名
        """
        # 判断操作目录是否是授权目录，或者授权目录的子目录
        if cur_resource.find(self.resource) != 0:
            raise ErrException(ERROR.E40306)

        if 'range' not in self.json or key not in self.json['range']:
            raise ErrException(ERROR.E40000, extra='wrong range key of %s' % key)

        return self.json['range'][key]

    def _key(self, nonce=''):
        return f'{config.DOMAIN}/license/{self.authority}/{tools.gen_md5(self.resource + self.owner)}/{nonce}'
