from distutils.core import setup

with open('README') as file:
    long_description = file.read()


setup(
  name='febase62',
  packages=['febase62'],  # this must be the same as the name above
  version='1.2.1',
  description='Base62 encoding',
  author='Friedrich Ewald',
  author_email='freddiemailster@gmail.com',
  url='https://bitbucket.org/f-ewald/febase62',  # use the URL to the github repo
  download_url='https://bitbucket.org/f-ewald/febase62/get/master.zip',
  keywords=['encoding'],
  classifiers=[],
)
