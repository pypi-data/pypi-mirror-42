import setuptools
import setuptools.command.test

class NoseTestCommand(setuptools.command.test.test):
    def finalize_options(self):
        setuptools.command.test.test.finalize_options(self)
        self.test_args = []
        self.test_suite = True
        
    def run_tests(self):
        import nose
        nose.run_exit(argv=["nosetests"])
        

with open("README.md", "r") as fd:
    long_description = fd.read()

setuptools.setup(
    name="bombfuse",
    version="0.3.2",
    author="The Munshi Group",
    author_email="support@munshigroup.com",
    description="Specify a timeout with any given function",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="timeout timed timer",
    url="https://github.com/munshigroup/bombfuse",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires = ['kthread'],
    tests_require = ['nose'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    cmdclass={"test": NoseTestCommand},
)