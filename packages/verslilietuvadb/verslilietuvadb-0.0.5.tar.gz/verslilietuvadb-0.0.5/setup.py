from setuptools import find_packages, setup

setup(
    name='verslilietuvadb',
    version='0.0.5',
    description='Versli Lietuva EDB controller.',
    url='https://gitlab.com/wefindx/verslilietuvaedb',
    author='Mindey',
    author_email='mindey@qq.com',
    license='ASK FOR PERMISSIONS',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires=['metadrive'],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    zip_safe=False
)
