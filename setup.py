"""
   Copyright 2021 Deutsche Telekom AG

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setuptools.setup(
    name="onap_data_provider",
    version="0.7.2",
    author="Michal Jagiello <michal.jagiello@t-mobile.pl>, Piotr Stanior <piotr.stanior@t-mobile.pl>, Pawel Denst <pawel.denst@external.t-mobile.pl>",
    description="Tool to provide data for ONAP instances",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="ONAP",
    packages=setuptools.find_packages(),
    package_data={"onap_data_provider": ["schemas/*"]},
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "onap-data-provider=onap_data_provider.data_provider:run",
        ]
    },
    install_requires=["onapsdk==12.3.2", "PyYAML~=5.4.1", "jsonschema==4.4.0"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
