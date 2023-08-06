from setuptools import setup, find_packages
import os
import io
import versioneer

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='shutilwhich-cwdpatch',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),

    description="Patch for shutil.which and shutilwhich that disables search in CWD on Windows.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url='https://github.com/kiwi0fruit/shutilwhich-cwdpatch',

    author='Peter Zagubisalo, Python Software Foundation',
    author_email='peter.zagubisalo@gmail.com',

    license='PSFL',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Python Software Foundation License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    packages=find_packages(exclude=['docs', 'tests']),
)
