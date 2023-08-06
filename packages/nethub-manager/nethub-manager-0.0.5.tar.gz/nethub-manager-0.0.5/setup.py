from setuptools import setup
from setuptools import find_packages


setup(name='nethub-manager',
      version='0.0.5',
      author='Nethub',
      author_email='nethub@yandex.ru',
      scripts=['manager/bin/nethub-manager.py'],
      entry_points={'console_scripts': [
          'nhm = manager.core.managment: execute_from_command_line'
      ]},
      install_requires=['h5py'],
      include_package_data=True,
      packages=find_packages()
)
