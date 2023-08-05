from setuptools import setup, find_packages 

with open('README.md') as f:
    long_description = f.read()

setup(name='divinegift',
      version='1.0.11.1',
      description='Live templates like PyCharm live templates in divinegift now!',
      long_description=long_description,
      long_description_content_type='text/markdown',  # This is important!
      classifiers=['Development Status :: 5 - Production/Stable',
                   'License :: OSI Approved :: MIT License',
                   'License :: OSI Approved :: Apache Software License',
                   'Programming Language :: Python :: 3',
                   "Operating System :: OS Independent", ],
      keywords='s7_it',
      url='https://gitlab.com/gng-group/divinegift.git',
      author='Malanris',
      author_email='admin@malanris.ru',
      license='MIT',
      packages=find_packages(),
      install_requires=['sqlalchemy', 'requests', 'mailer', 'xlutils', 'xlsxwriter', 'transliterate', 'cryptography'],
      include_package_data=True,
      zip_safe=False)