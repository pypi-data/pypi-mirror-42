import setuptools

long_description = open("README.md").read()

setup_params = dict(
    name="pr-publisher",
    version="0.0.1",
    license="MIT",
    author="Paul Glass",
    author_email="pnglass@gmail.com",
    url="https://github.com/pglass/pr-publisher",
    keywords="github slack pull request list publish remind",
    description="publish a list of open pull requests",
    packages=setuptools.find_packages(),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "PTable==0.9.2",
        "ConfigArgParse==0.14.0",
        "github3.py==1.3.0",
        "requests==2.21.0",
    ],
    entry_points={"console_scripts": ["pr-publisher = pr_publisher.cli:main"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)

if __name__ == "__main__":
    setuptools.setup(**setup_params)
