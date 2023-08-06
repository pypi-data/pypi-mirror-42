from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='streamdeck',
   version='0.1',
   description='Library to control Elgato StreamDeck devices.',
   author='Dean Camera',
   author_email='dean@fourwalledcubicle.com',
   packages=['src/StreamDeck', 'src/StreamDeck/Transport', 'src/StreamDeck/Devices'],
   install_requires=['hidapi'],
   license="MIT",
   long_description=long_description,
   long_description_content_type="text/markdown",
   include_package_data=True,
)
