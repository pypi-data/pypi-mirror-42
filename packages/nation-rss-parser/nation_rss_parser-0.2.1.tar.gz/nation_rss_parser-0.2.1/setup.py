import setuptools

with open('README.md','r') as file:
     long_description = file.read()

setuptools.setup(
    name='nation_rss_parser',
    version='0.2.1',
    author='Felix Mutugi',
    author_email='stunnerszone@gmail.com',
    descritpion='A RSS parser from https://www.nation.co.ke/ for Windows and has CMD support',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    packages=setuptools.find_packages(),
    classifiers=[
                 'Programming Language :: Python :: 3',
                 'Operating System :: Microsoft :: Windows :: Windows 7',
                 'License :: OSI Approved :: MIT License',
                 ],
    )    
