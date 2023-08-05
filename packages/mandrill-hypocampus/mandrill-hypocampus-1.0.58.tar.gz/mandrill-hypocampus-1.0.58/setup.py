from setuptools import setup
import os.path

setup(
    name='mandrill-hypocampus',
    version='1.0.58',
    author='Mandrill Devs & hypocampus',
    author_email='magnus.odman@gmail.com',
    description='A CLI client and Python API library for the Mandrill email as a service platform.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README')).read(),
    license='Apache-2.0',
    keywords='mandrill email api',
    url='https://gitlab.com/hypocampus/mandrill-api-python',
    scripts=['scripts/mandrill', 'scripts/sendmail.mandrill'],
    py_modules=['mandrill'],
    install_requires=['requests >= 2.21.0', 'docopt >= 0.6.2'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Communications :: Email'
    ]
)
