from setuptools import setup

setup(
    name="gradient_statsd",
    author="Paperspace",
    author_email="info@paperspace.com",
    version="0.1",
    url="https://www.paperspace.com",
    description="Wrapper around the DogStatsd client",
    license="MIT",
    packages=["gradient_statsd"],
    python_requires=">=2.7, >=3.4",
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "certifi==2018.11.29",
        "chardet==3.0.4",
        "datadog==0.26.0",
        "decorator==4.3.2",
        "idna==2.8",
        "requests==2.21.0",
        "urllib3==1.24.1",
    ],
)
