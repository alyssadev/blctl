from setuptools import setup, find_packages

setup(
    name="blctl",
    version="0.0.1",
    description="A Python CLI for BinaryLane's API",
    url="https://github.com/alyssadev/blctl",
    author="Alyssa Smith",
    author_email="alyssa.dev.smith@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=["requests", "appdirs"],
    entry_points={
        "console_scripts": [
            "blctl = blctl.blctl:main",
            "binarylanectl = blctl.blctl:main"
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License'
    ]
)
