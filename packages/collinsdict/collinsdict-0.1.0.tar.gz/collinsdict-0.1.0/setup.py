import setuptools

with open('README.md','r') as f:
    long_description = f.read()

setuptools.setup(
    name='collinsdict',
    version='0.1.0',
    author='liszt21',
    author_email='1832666492@qq.com',
    description='Collins Dictionary',
    long_description=long_description,
    long_description_content_type='text/plain',
    url='https://github.com/Lisz21/CollinsDict',
    packages=['collinsdict']
)
