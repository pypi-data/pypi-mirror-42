from setuptools import setup

setup(name='cwlbrowser',
      version='2.5',
      description='Python library that browses and analyses workflows in CWL',
      url='https://gitlab.cs.man.ac.uk/mbaxasp7/cwlbrowser',
      author='Sean Pertet',
      author_email='sean.pertet@student.manchester.ac.uk',
      packages=['cwlbrowser'],
      install_requires=[
          'pyyaml',
          'requests',
          'cwlref-runner',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False)