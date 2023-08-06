import os
import pathlib
import setuptools

VERSION = '0.14.0'

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

search_dirs = ['/usr', '/usr/local']

user_search_dir = os.environ.get('DRIVELINE_BASE_DIR')
if user_search_dir is not None:
    search_dirs.insert(0, user_search_dir)

video_module = setuptools.Extension(
    '_driveline_video',
    sources=['src/video.c'],
    include_dirs=list(map(lambda x: os.path.join(x, 'include'), search_dirs)),
    library_dirs=list(map(lambda x: os.path.join(x, 'lib'), search_dirs)),
    libraries=['dl_video_sdk'],
)

setuptools.setup(
    name='driveline-video',
    description='1533 Systems Driveline video decoder',
    version=VERSION,
    author='1533 Systems',
    url='https://github.com/1533-systems/python-sdk',
    author_email='info@1533.io',
    long_description=README,
    long_description_content_type='text/markdown',
    ext_modules=[video_module],
    keywords="driveline performance database streaming document",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6.0',
    install_requires=[
        'driveline~=%s' % VERSION,
    ]
)
