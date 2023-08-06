from distutils.core import setup
from setuptools import setup
from setuptools import find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="hd_llz",
    version="0.0.0.1",
    description="This is an installation package that detects the hand of the video.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    packages = find_packages(), 
    include_package_data = True,    # include everything in source control
    #packages = ['hd_llz', 'hd_llz/models', 'hd_llz/data'], 
    package_data = {
        'hd_llz':['models/v2_our6_rfcnmv_anchor12_320_500000', 'models/v2_our6_rfcnmv_anchor9_180_369818', 'data/test.png', 'data/hand_label_map.pbtxt']},

 
    license = "MIT",
    author="llz",
    author_email="hero1153@sina.com",
    #url='<null>',
    platforms = 'any',

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

