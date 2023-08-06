import setuptools
from setuptools import setup

setup(name='alphabox',
      version='0.0.1',
      description='Package to easily and programmatically interact with the BOX algorithm',
      url='https://github.com/yenicelik/alphabox',
      download_url='https://github.com/yenicelik/alphabox/archive/0.0.1.tar.gz',  # I explain this later on # TODO
      author='David Yenicelik',
      author_email='david@theaicompany.com',
      license='Mozilla Public License Version 2.0',
      packages=setuptools.find_packages(),
      zip_safe=False,
      keywords=['optimization', 'blackbox', 'bayesian', 'optimization', 'box', 'alpha'],  # Keywords that define your package best
      classifiers=[
            'Development Status :: 3 - Alpha',
            # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
            'Intended Audience :: Developers',  # Define that your audience are developers
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',  # Again, pick a license
            'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
      ],
      install_requires=[
            "requests==2.21.0",
            "hypothesis==4.7.2",
            "mock==2.0.0",
            "python-dotenv"
      ]
)