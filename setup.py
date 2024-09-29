from setuptools import find_packages, setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='VLQBounds',
    version="0.1",
    description='Python code to check LHC upper limits on Vector-like quarks parameters.',
    package_dir={'': 'vlqBounds'},
    packages=find_packages(where='vlqBounds'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/HEP-VLQ/VLQBounds',
    author='Rachid Benbrik, Mohamed Boukidi, Ech-chaouy Mohamed, Salime khawla',
    author_email='r.benbrik@uca.ac.ma, mohammed.boukidi@ced.uca.ac.ma, '
                 'm.echchaouy.ced@uca.ac.ma, k.salime.ced@uca.ac.ma',
    license='MIT',
    install_requires= [
    'numpy',
    'scipy', 
    'pandas'
    ],
    python_requires=">=3.8",

)
