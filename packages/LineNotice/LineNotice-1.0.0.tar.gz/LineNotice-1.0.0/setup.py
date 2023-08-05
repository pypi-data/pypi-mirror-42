from setuptools import setup, find_packages
import LineNotice

setup(
    name="LineNotice",
    version=LineNotice.__version__,
    description="Notice to LINE.",
    license=LineNotice.__license__,

    author=LineNotice.__author__,
    author_email="syukatsu_chubu@yahoo.co.jp",

    # packages=find_packages(exclude=[None]),

    install_requires=["requests"],
)