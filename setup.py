from setuptools import find_packages, setup

import versioneer

setup(
    name="DOE2-SIM-Parser",
    author="Grammy Jiang",
    author_email="grammy.jiang@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Topic :: Terminals",
    ],
    cmdclass=versioneer.get_cmdclass(),
    include_package_data=True,
    install_requires=["gspread", "oauth2client"],
    license="BSD",
    maintainer="Grammy Jiang",
    maintainer_email="grammy.jiang@gmail.com",
    packages=find_packages(exclude=("tests", "tests.*")),
    url="https://github.com/grammy-jiang/doe2-sim-parser",
    version=versioneer.get_version(),
    zip_safe=False,
)
