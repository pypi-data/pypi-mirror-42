# -*- coding: utf-8 -*-

################################################################
# xmldirector.connector
# (C) 2019,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################

from zope import schema
from zope.interface import Interface
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from xmldirector.plonecore.i18n import MessageFactory as _


class IBrowserLayer(Interface):
    """A brower layer specific to my product """


class IConnectorHandle(Interface):
    """ Return a DAVFS handle for the system-wide configured conector handle """


class ITransformerRegistry(Interface):
    """ Marker interface for TransformerRegistry """


class IValidatorRegistry(Interface):
    """ Marker interface for ValidatorRegistry """


CONNECTOR_MODE_VOCAB = SimpleVocabulary([
    SimpleTerm('existdb', title='Exist-DB'),
    SimpleTerm('basex', title='BaseX'),
    SimpleTerm('alfresco', title='Alfresco'),
    SimpleTerm('dropbox-dropdav', title='Dropbox (via dropdav.com)'),
    SimpleTerm('owncloud', title='OwnCloud'),
    SimpleTerm('other', title='Other')
])


class IConnectorSettings(Interface):
    """ Connector settings """

    connector_url = schema.TextLine(
        title=_('Connection URL of storage'),
        description=_('WebDAV: http://host:port/path/to/webdav,'
                      'Local filesystem: file://path/to/directory, '
                      'AWS S3: s3://bucketname, SFTP sftp://host/path, '
                      'FTP: ftp://host/path'),
        default='',
        required=True)

    connector_username = schema.TextLine(
        title=_('Username for external storage'), description=_('Username'), default='admin', required=False)

    connector_password = schema.Password(
        title=_('Password external storage'), description=_('Password'), default='', required=False)

    connector_mode = schema.Choice(
        title=_('Connector mode'),
        description=_('Connector mode (defaults to \'Other\')'),
        default='other',
        required=True,
        vocabulary=CONNECTOR_MODE_VOCAB)

    connector_dexterity_subpath = schema.TextLine(
        title=_('Dexterity subpath'),
        description=_('Subpath inside storage for Dexterity content'),
        default='',
        required=False)
