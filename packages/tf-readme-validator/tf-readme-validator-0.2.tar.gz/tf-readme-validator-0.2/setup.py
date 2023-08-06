from setuptools import setup

setup(name='tf-readme-validator',
      version='0.2',
      description='Terraform README.md validator',
      url='https://github.com/lean-delivery/tf-readme-validator',
      author='Lean Delivery team',
      author_email='team@lean-delivery.com',
      license='Apache',
      scripts=['bin/tf_readme_validator.py'],
      install_requires=[
        'pyyaml',
        'mistune',
      ],
      zip_safe=False)
