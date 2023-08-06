from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pylodash',
    version='0.3.0',
    description='A modern Python utility library delivering modularity, performance & extras.',
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords='python lodash utilities',
    url='https://gitlab.asoft-python.com/g-tuanluu/python-training',
    author='Tuan Luu',
    author_email='tuan.luu@asnet.com.vn',
    license='MIT',
    packages=['src'],
    install_requires=[
        'markdown',
    ],
    test_suite='nose2.collector.collector',
    tests_require=['nose2'],
    include_package_data=True,
    zip_safe=False)