from setuptools import setup, find_packages


setup(
    name='xwklwwltestpackage',
    license='Apache License 2.0',
    version='0.0.3',
    # packages=['testpackage'],
    packages=find_packages(where='.', exclude=(), include=('*',)),
    zip_safe=False,
    include_package_data=True,
    url='https://github.com/xwklwwlf/testpackage',
    author='xwklwwlf',
    author_email='xwklwwlf@gmail.com',
    description='test',
    install_requires=[],
    )
