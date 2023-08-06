import os

__import__('pkg_resources').declare_namespace(__name__)


# assumes running from root deploy_utils folder, so need to go one level deeper
BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
CONFIG_DIR = os.path.join(BASE_DIR, 'config')
