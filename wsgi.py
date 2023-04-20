import os

from app import create_app
from app.libs.providers.viva_provider import VivaProvider

env = os.environ.get('ENV', 'development')

provider = VivaProvider()
app = create_app(provider=provider, env=env)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
