from setuptools import setup, find_packages


setup(name='x-mroy-1050',
    version='0.2.9.1',
    description=' x-mroy',
    url='https://github.com/Qingluan/.git',
    author='Qing luan',
    author_email='darkhackdevil@gmail.com',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    install_requires=['termcolor', 'mroylib-min',],
    entry_points={
        'console_scripts': [
            'x-sstest=shadowsocks_extension.test_route:main',
            'x-ea-test=shadowsocks_extension.test_route:sync_main',
            'x-sspatch=shadowsocks_extension.sspatch:main',
            ]
    },

)
