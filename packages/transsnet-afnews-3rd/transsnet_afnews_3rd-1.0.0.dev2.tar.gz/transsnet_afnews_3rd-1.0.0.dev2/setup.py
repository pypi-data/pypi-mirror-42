from setuptools import setup
from setuptools import find_packages


setup(
        name='transsnet_afnews_3rd',     # 包名字
        version='1.0.0.dev2',   # 包版本（每次需要更新这个再推到git上）
        description='africa news third party project',   # 简单描述
        url='https://git.ms.netease.com/africaNews/transsnet_afnews_3rd',      # 包的主页
        packages=find_packages()            # 部署的包，这里不需要部署，只是通过setup.py来安装需要的依赖
        # install_requires=[
        #         'redis',
        #         'pymongo',
        #         'sqlalchemy',
        #         'flask',
        #         'transsnet-afnews-common'
        # ] # 需要的依赖， 后面可以跟 ">1.0" 表示需要的最小版本号
)

