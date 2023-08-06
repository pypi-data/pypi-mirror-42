#! /usr/local/bin/python3
# encoding: utf-8
# Author: LiTing

import os
import sys
import getopt
import requests
import base64
import json
import re

# add search path
sys.path.append(os.path.abspath(os.path.curdir))
from .utils import *


def print_help():
    print('\n 功能：'
          '\n\t 1. 对比Android的properties的最新版本号'
          '\n\t 2. 对比iOS的Podfile的最新版本号'
          '\n\t 3. 对比iOS的Podfile.lock的最新版本号'
          '\n'
          '\n 数据源：'
          '\n\t 1. 本地：.properties、Podfile、Podfile.lock、最新的版本号文件.cfg'
          '\n\t 2. 网络：最新的版本号文件.cfg（存于gitlab上）'
          '\n'
          '\n 命令：'
          '\n\t python3 xxx.py [-a <android-properties>] [-i <ios-podfile>] [-k <ios-podfile.lock>] -v <lastest-version-config> [-h]'
          '\n 参数：'
          '\n\t -a: 表示Android的properties文件（本地或网络url）'
          '\n\t -i: 表示iOS的Podfile文件（本地或网络url）'
          '\n\t -k: 表示iOS的Podfile.lock文件（本地或网络url）'
          '\n\t -v: 表示最新版本配置文件（本地或网络url）'
          '\n\t -h: 表示帮助'
          '\n'
          )


"""
    CONFIG.json
    
        {
            "iOS" : {
                "---库名---" : "---最新的版本号---",
        
                "---网络库---" : "------",
                "NetworkSDK" : "6.2.1.24"
            },
        
            "Android" : {
                "---库名---" : "---最新的版本号---",
        
                "---网络库---" : "------",
                "com.taobao.android.networksdk.version" : "3.3.8.2"
            }
        }



    DONE:
        1. 每个库当前版本与最新的版本号对比
    TODO:
        1. 引入的库（一方、二方、三方）个数
        2. 每个库的类型（源码、二进制包）
        3. 未打tag的库
"""


def main(argv):
    # parse args
    try:
        opts, args = getopt.getopt(argv, 'a:i:k:v:h', ['android-properties=', 'ios-podfile=', 'ios-podfile-lock=',
                                                       'lastest-version-config=', 'help'])
    except getopt.GetoptError:
        print('python3 xxx.py [-a <android-properties>] [-i <ios-podfile>] [-k <ios-podfile.lock>] -v <lastest-version-config>')
        sys.exit(2)

    # 默认值
    android_properties = ''
    ios_podfile = ''
    ios_podfilelock = ''
    lastest_version_config = ''

    # 解析参数
    for opt, arg in opts:
        if opt in {'-a', '--android-properties'}:
            android_properties = arg
        elif opt in {'-i', '--ios-podfile'}:
            ios_podfile = arg
        elif opt in {'-k', '--ios-podfile-lock'}:
            ios_podfilelock = arg
        elif opt in {'-v', '--lastest-version-config'}:
            lastest_version_config = arg
        elif opt in {'-h', '--help'}:
            print_help()
            return

    # 入口函数调用
    do_check(android_properties, ios_podfile, ios_podfilelock, lastest_version_config)


def do_check(properties, podfile, podfilelock, lastest_version_config_path):
    PrintWithColor.blue('\n-> begin .py')

    # verify files
    PrintWithColor.blue('-> checking files valid...')

    # lastest config json
    lastest_config_json = {}
    if os.path.isfile(lastest_version_config_path):
        with open(lastest_version_config_path, encoding='utf-8') as f:
            lastest_config_json = json.loads(f.read())
    else:
        if not lastest_version_config_path.startswith('http'):
            PrintWithColor.blue(f'[!] <{lastest_version_config_path}> is a invalid config url.')
            PrintWithColor.blue('-> end \n')
            return

        try:
            PrintWithColor.blue(f'-> requesting url: {lastest_version_config_path}')
            # request url
            r = requests.get(lastest_version_config_path)

            # response json
            json_text = r.json()

            # 获取文件内容
            json_content = json_text.get('content')

            # 编解码
            json_content = base64.b64decode(json_content)  # base64解码
            json_content = str(json_content, encoding='utf-8')  # 一定要utf-8编码一次

            # json格式化
            lastest_config_json = json.loads(json_content)

            # request success
            PrintWithColor.blue('-> request successfully.')
        except Exception as e:
            PrintWithColor.red(f'[!] error type: {type(e)}')
            PrintWithColor.red(f'[!] error: {e}')
            PrintWithColor.red(f'[!] <local-config-path> and <local-config-url> are both invalid.')
            return

    if len(lastest_config_json) <= 0:
        PrintWithColor.red(f'[!] config json has no pairs.')
        PrintWithColor.blue('-> end \n')
        return

    # using version files
    is_valid_properties = False
    is_valid_podfile = False
    is_valid_podfilelock = False

    if os.path.isfile(properties) or properties.startswith('http'):
        is_valid_properties = True
    if os.path.isfile(podfile) or podfile.startswith('http'):
        is_valid_podfile = True
    if os.path.isfile(podfilelock) or podfilelock.startswith('http'):
        is_valid_podfilelock = True

    if not is_valid_properties and not is_valid_podfile and not is_valid_podfilelock:
        PrintWithColor.red('[!] no valid Android or iOS files are available. '
                           'specify: version.properties | Podfile | Podfile.lock')
        return

    # Android properties checker
    if is_valid_properties:
        android_properties_checker = AndroidPropertiesChecker(properties, lastest_config_json)
        android_properties_checker.do_run()

    # iOS podfile checker
    if is_valid_podfile:
        ios_podfile_checker = IOSPodfileChecker(podfile, lastest_config_json)
        ios_podfile_checker.do_run()

    # iOS podfile.lock checker
    if is_valid_podfilelock:
        ios_podfilelock_checker = IOSPodfileLockChecker(podfilelock, lastest_config_json)
        ios_podfilelock_checker.do_run()

    # end
    PrintWithColor.blue('-> end .py\n')


# ------------------------------------------------------

class Pod(object):
    name = ''
    version = ''

    def __init__(self, name, version):
        self.name = name
        self.version = version

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not (self == other)


class PodChecker(object):
    using_config_file = ''
    lastest_config_json = {}

    using_pods = []
    lastest_pods = []

    def __init__(self, using_config_file, lastest_config_json):
        self.using_config_file = using_config_file
        self.lastest_config_json = lastest_config_json
        self.using_pods = []
        self.lastest_pods = []

    def _parse_using_file(self, pattern):
        f_text = ''
        if os.path.isfile(self.using_config_file):
            PrintWithColor.blue(f'-> parsing file path: {self.using_config_file}')
            with open(self.using_config_file, encoding='utf-8') as f:
                f_text = f.read()
        elif self.using_config_file.startswith('http'):
            PrintWithColor.blue(f'-> requesting file url: {self.using_config_file}')
            r = requests.get(self.using_config_file)
            f_text = r.text

        ai = re.compile(pattern).findall(f_text)
        if ai is not None:
            pod_dict = {t[0]: t[1] for t in ai}
            for pod in self._unique_generator(self.using_pods, pod_dict):
                self.using_pods.append(pod)

    def _parse_compare_file(self, platform):
        cfs = self.lastest_config_json.get(platform, {})
        cfs_dict = {x: cfs.get(x) for x in cfs if not x.startswith('---')}

        for pod in self._unique_generator(self.lastest_pods, cfs_dict):
            self.lastest_pods.append(pod)

        # self.lastest_pods.append(pod) if pod not in self.lastest_pods else _

    def _unique_generator(self, pods, config_dicts):
        for x in config_dicts:
            tmp_pod = Pod(x, config_dicts.get(x))
            if tmp_pod not in pods:
                yield tmp_pod

    def _compare(self):
        class _PodCompareInfo(object):
            name = ''
            using_version = ''
            lastest_version = ''

            def __init__(pself, name, using_version, lastest_version):
                pself.name = name; pself.using_version = using_version; pself.lastest_version = lastest_version

            def debug_infos(pself):
                eq_version = pself.using_version == pself.lastest_version
                return _debug_print_format(pself.name, pself.using_version, pself.lastest_version,
                                           eq_version, not eq_version)

        pod_compare_infos = []
        for l_pod in self.lastest_pods:
            for r_pod in self.using_pods:
                if l_pod == r_pod:
                    pod_compare_infos.append(_PodCompareInfo(l_pod.name, r_pod.version, l_pod.version))

        def _debug_print_format(arg1, arg2, arg3, arg4, specifiedcolor=False):
            if specifiedcolor:
                arg4 = PrintWithColor.simple_preferred_formatted_string(kFore.RED, arg4)
            return f'{arg1:<{self._debug_format_num()}s} {arg2:<14s} {arg3:<18s} {arg4}'

        PrintWithColor.yellow(_debug_print_format('pod_name', 'using_version', 'lastest_version', 'up_to_date'))
        PrintWithColor.yellow(_debug_print_format('--------', '-------------', '---------------', '----------'))
        for x in pod_compare_infos[-4:]:
            PrintWithColor.yellow(x.debug_infos())
        # PrintWithColor.yellow('\n'.join((x.debug_infos() for x in pod_compare_infos)))
        PrintWithColor.yellow(_debug_print_format('--------', '-------------', '---------------', '----------'))

    def _debug_format_num(self):
        return 10

    def do_run(self):
        self._parse_using_file()
        self._parse_compare_file()
        self._compare()


class AndroidPropertiesChecker(PodChecker):
    def __init__(self, using_config_file, lastest_config_json):
        PodChecker.__init__(self, using_config_file, lastest_config_json)

    def _parse_using_file(self):
        super()._parse_using_file(r'(.+?)=(.+)')

    def _parse_compare_file(self):
        super()._parse_compare_file('Android')

    def _debug_format_num(self):
        return 60

    def do_run(self):
        PrintWithColor.green('\n-> begin to check Android version.properties')
        super().do_run()
        PrintWithColor.green('-> end to check Android version.properties\n')
        # say


class IOSPodfileChecker(PodChecker):
    def __init__(self, using_config_file, lastest_config_json):
        PodChecker.__init__(self, using_config_file, lastest_config_json)

    def _parse_using_file(self):
        super()._parse_using_file(r'pod[\s]+\'(.+?)\'[\s]*,[\s]*\'(.+?)\'')

    def _parse_compare_file(self):
        super()._parse_compare_file('iOS')

    def _debug_format_num(self):
        return 20

    def do_run(self):
        PrintWithColor.green('\n-> begin to check iOS Podfile')
        super().do_run()
        PrintWithColor.green('-> end to check iOS Podfile \n')
        # say


class IOSPodfileLockChecker(PodChecker):
    def __init__(self, using_config_file, lastest_config_json):
        PodChecker.__init__(self, using_config_file, lastest_config_json)

    def _parse_using_file(self):
        super()._parse_using_file(r'-[\s]*(.+?)[\s]*\([=~>\s]*(.+?)\)')

    def _parse_compare_file(self):
        super()._parse_compare_file('iOS')

    def _debug_format_num(self):
        return 20

    def do_run(self):
        PrintWithColor.green('\n-> begin to check iOS Podfile.lock')
        super().do_run()
        PrintWithColor.green('-> end to check iOS Podfile.lock \n')
        # say

# ------------------------------------------------------


if "__main__" == __name__:
    main(sys.argv[1:])
