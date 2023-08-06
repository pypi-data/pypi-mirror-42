import flamingo

# plugins
CORE_PLUGINS = [
    'flamingo.core.plugins.MetaDataProcessor',
]

DEFAULT_PLUGINS = [
    'flamingo.plugins.HTML',
    'flamingo.plugins.reStructuredText',
    'flamingo.plugins.rstImage',
    'flamingo.plugins.rstFile',
]

PLUGINS = []

# parsing
USE_CHARDET = False
TYPE_EVALUATION = True

# templating
TEMPLATING_ENGINE = 'flamingo.core.templating.Jinja2'
EXTRA_CONTEXT = {}

CORE_THEME_PATHS = [
    flamingo.THEME_ROOT,
]

THEME_PATHS = []

DEFAULT_TEMPLATE = 'page.html'

DEFAULT_PAGINATION = 25

# content
CONTENT_ROOT = 'content'
CONTENT_PATHS = []

# output
OUTPUT_ROOT = 'output'
MEDIA_ROOT = 'output/media'
STATIC_ROOT = 'output/static'
