from setuptools import setup

setup(
    name='firetv',
    version='1.0.8',
    description='Communicate with an Amazon Fire TV device via ADB over a network.',
    url='https://github.com/happyleavesaoc/python-firetv/',
    license='MIT',
    author='happyleaves',
    author_email='happyleaves.tfr@gmail.com',
    packages=['firetv'],
    install_requires=['pycryptodome', 'rsa', 'adb-homeassistant', 'pure-python-adb-homeassistant'],
    extras_require={
        'firetv-server': ['Flask>=0.10.1', 'PyYAML>=3.12']
    },
    entry_points={
        'console_scripts': [
            'firetv-server = firetv.__main__:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ]
)
