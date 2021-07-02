from setuptools import setup, find_packages
import pathlib

CWD = pathlib.Path(__file__).parent

README = (CWD / "README.md").read_text()

setup(
    name='MirrorX',
    version='6.0.0',
    packages=find_packages(),
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/iamliquidx/mirrorx',
    license='GPL3.0',
    author='',
    author_email='',
    include_package_data=True,
    description='Telegram Mirror Bot',
    platforms="any",
    install_requires=[
        "requests",
        "appdirs",
        "aria2p",
        "progress",
        "psutil",
        "python-telegram-bot",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "js2py",
        "python-dotenv",
        "tenacity",
        "python-magic",
        "beautifulsoup4",
        "Pyrogram",
        "TgCrypto",
        "yt-dlp",
        "lxml",
        "telegraph",
        "speedtest-cli",
        "messages",
        "pybase64",
        "lk21",
        "megasdkrestclient"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 5 - Production/Stable"
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts":[
            "MirrorX = bot.__main__:main"
        ]

    },
    package_data={
        "": ["data/*.dat", "data/aria.conf"],
    },
    scripts=['bin/extract', 'bin/pextract'],
)