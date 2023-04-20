from setuptools import setup, find_packages

setup(
    name="gpt-assistant",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gpt-assistant = gpt_assistant.__main__:main',
        ],
    },
    install_requires=[],
)
