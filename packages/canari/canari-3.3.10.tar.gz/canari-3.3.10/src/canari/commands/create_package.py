from datetime import datetime
from distutils.version import StrictVersion
from getpass import getuser
from os import path

import click
from mrbob.configurator import Configurator

import canari

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'


def create_package(package_name, author, email, description, create_example):

    capitalized_package_name = package_name.capitalize()

    variables = {
        'project.name': package_name,
        'project.description': description,
        'project.create_example': create_example,
        'entity.example_name': 'My%sEntity' % capitalized_package_name,
        'entity.base_name': '%sEntity' % capitalized_package_name,
        'created.year': datetime.now().year,
        'canari.version': canari.version,
        'canari.major_version': StrictVersion(canari.version).version[0],
        'author.name': author,
        'author.email': email
    }

    if not path.exists(package_name):
        click.echo('creating skeleton in %s' % package_name, err=True)
        configurator = Configurator(
            'canari.resources.templates:create_package%s' % ('' if create_example else '_no_example'),
            package_name,
            {'non_interactive': True, 'remember_answers': True},
            variables=variables
        )
        configurator.ask_questions()
        configurator.render()
    else:
        click.echo('A directory with the name %s already exists... exiting' % package_name, err=True)
        exit(-1)

    click.echo('done!', err=True)
