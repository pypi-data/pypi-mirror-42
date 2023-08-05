from distutils.core import setup

setup(
    name="jdcpy",
    author="JaydenFish@ThizGroup",
    author_email="xmyjd@163.com",
    version="1.2.1",
    py_modules=['jdcpy', 'paramConverter'],
    install_requires=['pandas', 'requests'],
    description="jdcpy模块,吉富数据中心的python接口",
    long_description=open("JDKSDK使用说明.md", encoding='utf8').read()
)
