#!/usr/bin/python


import os
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


proj_dir = os.path.dirname(os.path.realpath(__file__))
requirements_path = os.path.join(proj_dir, 'requirements.txt')
install_requires = []
if os.path.isfile(requirements_path):
    with open(requirements_path) as f:
        install_requires = f.read().splitlines()

# install_requires += [
#     'db_update@git+https://github.com/netgroup/rose-srv6-control-plane@add-setup#"subdirectory=db_update-0.0.1/db_update&egg=db_update-0.0.1"',
#     # 'rose-srv6-control-plane-protos@git+https://github.com/netgroup/rose-srv6-control-plane@add-setup#egg=rose-srv6-control-plane-protos-0.0.1&subdirectory=control_plane/protos',
#     #'db_update==0.0.1'
# ]

# dependency_links = [
#     # 'https://github.com/netgroup/rose-srv6-control-plane/tarball/add-setup#egg=rose-srv6-control-plane-protos&subdirectory=control_plane/protos',
#     'https://github.com/netgroup/rose-srv6-control-plane/tarball/add-setup#"subdirectory=db_update&egg=db_update-0.0.1"',
# ]

packages = [
    '',
    'cli'
]

setuptools.setup(
    name="rose-srv6-control-plane-controller",
    version="0.0.1",
    author="Carmine Scarpitta",
    author_email="carmine.scarpitta@uniroma2.it",
    description="Collection of control-plane modules for a Controller",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/netgroup/rose-srv6-control-plane",
    packages=packages,
    install_requires=install_requires,
    # dependency_links=dependency_links,
    entry_points={'console_scripts': ['controller = controller:__main']},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Linux',
        'Programming Language :: Python',
    ],
    python_requires='>=3.6'
)
