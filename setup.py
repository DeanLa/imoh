from setuptools import setup, find_packages
import versioneer

setup(
    name='imoh',
    author='Dean Langsam',
    url='https://github.com/DeanLa/IMoH',
    license="MIT",
    version = '0.1',
    # version=versioneer.get_version(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        imoh=imoh.scripts.cli:cli
    ''',
    keywords='python health',
)