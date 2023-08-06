from setuptools import find_packages, setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='beeflow',
    version='0.0.2',
    description='BeeML',
    long_description=readme(),
    platforms=['any'],
    packages=find_packages(),
    include_package_data=True,
    url='',
    license='Apache v2.0',
    author='Dae-Won Kim',
    author_email='dwkim78@gmail.com',
    install_requires=['pandas', 'plotly',
                      'dash', 'dash_table',
                      'dash_core_components',
                      'dash_html_components',
                      'dash_resumable_upload'],
    keywords=[''],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ]
)
