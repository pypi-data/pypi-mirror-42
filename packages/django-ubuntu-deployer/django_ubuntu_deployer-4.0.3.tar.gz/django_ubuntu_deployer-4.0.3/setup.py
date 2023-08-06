from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='django_ubuntu_deployer',
      version='4.0.3',
      description='Simple way to deploy Django app in Ubuntu Server.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/Maksych/django_ubuntu_deployer',
      author='Maksym Sichkaruk',
      author_email='maxim.18.08.1997@gmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)
