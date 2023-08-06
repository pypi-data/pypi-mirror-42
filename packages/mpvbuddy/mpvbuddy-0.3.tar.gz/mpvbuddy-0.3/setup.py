from setuptools import setup, find_packages

setup(
    name='mpvbuddy',
    version='0.3',
    packages=find_packages(),
    author='Sumit Khanna',
    author_email='sumit@penguindreams.org',
    url='https://battlepenguin.com',
    license='GNU General Public License v3',
    long_description='QT based frontend for the mpv media player supporting playlists and location bookmarking',
    entry_points={'console_scripts': ['mpvbuddy=mpvbuddy.__main__:main']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Multimedia :: Video',
        'Topic :: Multimedia :: Video :: Display'
    ],
    install_requires=['yoyo-migrations==6.0.0', 'python-mpv==0.3.9', 'PyQT5>=5.10']
)
