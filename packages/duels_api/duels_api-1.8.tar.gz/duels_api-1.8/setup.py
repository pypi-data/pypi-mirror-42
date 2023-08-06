from setuptools import setup, find_packages

setup(name='duels_api',
      version='1.8',
      include_package_data=True,
      description='Wrapper for API',
      url='https://github.com/Forevka69/DuelsGameBot',
      author='Forevka',
      author_email='zebestforevka@gmail.com',
      packages=find_packages(),
      #scripts=['objects/item.py', 'objects/user.py','objects/clan.py'],
      package_data={
        'objects': ['*.py'],
    })
