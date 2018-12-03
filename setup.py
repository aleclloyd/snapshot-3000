from setuptools import setup
setup(name='snapshot-3000',
      version='0.1',
      author='Alec Lloyd',
      author_email='boxesofbiscuit@gmail.com',
      description='Tool to manage EC2 instances',
      license='GPLv3+',
      packages=['shotty'],
      url='https://github.com/aleclloyd/snapshot-3000',
      install_requires=['click','boto3'],
      entry_points='''
      [console_scripts]
      shotty=shotty.shotty:cli
      ''')
