from setuptools import setup, find_packages
# import LineNotice

setup(
    name="LineNotice",
    # version=LineNotice.__version__,
    version = "1.0.1",
    description="Notice to LINE.",
    license="MIT",

    author="yoshida",
    author_email="syukatsu_chubu@yahoo.co.jp",

    # packages=find_packages(exclude=[None]),

    install_requires=["requests"],
)