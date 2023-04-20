import os
from app import create_app

env = os.environ.get('ENV', 'development')
app = create_app(env=env)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
