import setuptools

with open('README.org','r') as f:
    long_description = f.read()

setuptools.setup(
    name='collinsdict',
    version='0.0.1',
    author='liszt21',
    author_email='1832666492@qq.com',
    description='Collins Dictionary',
    long_description=long_description,
    long_description_content_type='text/plain',
    url='https://github.com/Lisz21/CollinsDict',
    packages=setuptools.find_packages()
)
