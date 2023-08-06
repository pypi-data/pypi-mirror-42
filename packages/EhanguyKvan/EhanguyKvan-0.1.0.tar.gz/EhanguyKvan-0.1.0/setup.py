from setuptools import setup, find_packages

setup(
    name = "EhanguyKvan",
    version = "0.1.0",
    keywords = ("pip", "codemao"),
    description = "自制的一个杂库，目前推广于codemao平台",
    license = "MIT Licence",

    url = "https://github.com/fengmm521/pipProject",
    author = "EhanguyKvan",
    author_email = "1162971013@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['wordcloud', 'scipy.misc', 'jieba', 'matplotlib']
)
