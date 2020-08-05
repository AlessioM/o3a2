from setuptools import find_packages, setup

setup(
    name="o3a2",
    version="0.1",
    author="AlessioM",
    author_email="",
    url="https://github.com/AlessioM/o3a2",
    packages=find_packages(include=['o3a2.*']),
    install_requires=[],
    setup_requires=[
    ],
    python_requires='>=3.6',
    test_suite='tests',
    tests_require=[],
    zip_safe=False,
    include_package_data=True,
)
