from setuptools import setup, find_namespace_packages

setup(
    name='cleaner',
    version='1.0.0',
    description='Sorting files',
    url='https://github.com/smilecool2012/goit-python/blob/master/DZ_6_sort/sort.py',
    author='Dima Mykytiuk',
    author_email='smilecool2012@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}
)
