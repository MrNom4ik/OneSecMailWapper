from distutils.core import setup

setup(name='OneSecMailWapper',
      description='Sync wapper over https://www.1secmail.com API temporary mail service',
      version='2.0.0',
      author='MrNom4ik',
      url='https://github.com/MrNom4ik/OneSecMailWapper',
      license='BY-NC-SA-4.0',
      install_requires=['requests', 'pydantic'],
      packages=['OneSecMailWapper']
      )
