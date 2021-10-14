
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nested-multipart-parser",
    version="0.1.0",
    author="Example Author",
    license='MIT',
    author_email='contact@germainremi.fr',
    description="A parser for nested data in multipart form",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/remigermain/nested-multipart-parser",
    project_urls={
        "Bug Tracker": "https://github.com/remigermain/nested-multipart-parser/issues",
    },
    classifiers=[
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: MIT License'
    ],
    package_dir={"": "src"},
    packages=["nested_multipart_parser"],
    python_requires=">=3.6",
)
