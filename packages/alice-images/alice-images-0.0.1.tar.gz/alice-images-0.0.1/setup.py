import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='alice-images',
    version='0.0.1',
    author='Aleksandr Alekseev',
    author_email='alekseevavx@gmail.com',
    description='Work with alice skills images: upload|list|delete',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AlekseevAV/alice-images',
    packages=setuptools.find_packages(),
    keywords='yandex alice images',
    install_requires=[
        'Click',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        alice_images=alice_images.cli:cli
    ''',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
