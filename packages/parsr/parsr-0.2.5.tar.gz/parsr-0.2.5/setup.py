from setuptools import setup, find_packages

develop = set([
    'ipython',
    'pytest',
    'setuptools',
    'twine',
    'wheel',
])


if __name__ == "__main__":
    setup(
        name="parsr",
        version="0.2.5",
        description="Parsr is a simple parser combinator library in pure python.",
        long_description=open("README.md").read(),
        long_description_content_type='text/markdown',
        url="https://github.com/csams/parsr",
        packages=find_packages(),
        package_data={'': ['LICENSE']},
        license='Apache 2.0',
        extras_require={
            'develop': list(develop),
        },
        classifiers=[
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7'
        ],
        include_package_data=True
    )
