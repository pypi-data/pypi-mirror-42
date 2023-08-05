import setuptools

def readme():
    with open("README.rst", "r") as f:
        return f.read()


with open('dextract/__init__.py') as fid:
    for line in fid:
        if line.startswith('__version__'):
            VERSION = line.strip().split()[-1][1:-1]
            break

setuptools.setup(name='dextract',
                 version=VERSION,
                 url='http://github.com/csehdz/dextract',

                 author='cseHdz',
                 author_email='carlos.hdz@me.com',

                 description='Layered extractor of data',
                 long_description = readme(),

                 license='MIT',

                 packages=setuptools.find_packages(exclude=['contrib', 'docs',
                                                            'tests*']),

                 install_requires=['pandas>=0.9.1',
                                   'numpy>=1.15.4',
                                   'xlrd>=1.2.0',
                                   'pyexcel>=0.5.10',
                                   'pyexcel-xls>=0.5.8',
                                   'pyexcel-xlsx>=0.5.7',
                                   'statistics>=1.0.3.5'],
                 python_requires='>=3',
                 zip_safe=False,

                 classifiers=[
                    'Programming Language :: Python :: 3',
                    'Operating System :: OS Independent'])
