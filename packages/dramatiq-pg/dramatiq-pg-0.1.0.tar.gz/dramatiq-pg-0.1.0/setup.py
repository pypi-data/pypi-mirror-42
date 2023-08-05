# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dramatiq_pg']

package_data = \
{'': ['*']}

install_requires = \
['dramatiq>=1.5,<2.0', 'psycopg2>=2.7,<3.0']

setup_kwargs = {
    'name': 'dramatiq-pg',
    'version': '0.1.0',
    'description': 'Postgres Broker for Dramatiq Task Queue',
    'long_description': '=============================================\n dramatiq-pg -- Postgres Broker for Dramatiq\n=============================================\n\ndramatiq_ is a simple task queue implementation for Python3. dramatiq-pg\nprovides a Postgres-based implementation of a dramatiq broker.\n\n**The project is not feature complete yet.**\n\n\nFeatures\n========\n\n- Super simple deployment.\n- Stores messages in a single table.\n- All data are wrapped in a dedicated schema.\n- Uses LISTEN/NOTIFY to keep worker sync. No polling.\n- Reliable thanks to Postgres MVCC.\n- Using plain psycopg2. No ORM.\n\n\nInstallation\n============\n\n- Install dramatiq-pg package from PyPI::\n\n      pip install dramatiq-pg\n\n- Apply dramatiq_pg/schema.sql file in your database::\n\n      psql -f dramatiq_pg/schema.sql\n\n- Before importing actors, define global broker with a connection pool::\n\n      import dramatiq\n      import dramatiq_pg\n      import psycopg2.pool\n\n      pool = psycopg2.pool.ThreadedConnectionPool(0, 4, conninfo)\n      dramatiq.set_broker(dramatiq_pg.PostgresBroker(pool=pool))\n\nNow declare/import actors and manage worker just like any `dramatiq setup\n<https://dramatiq.io/guide.html>`_.\n\n\nRoadmap\n=======\n\n- Process missed notifyes while resuming worker.\n- Functionnal tests.\n- Result storage as JSONb.\n- Delayed task.\n\n\n.. _dramatiq:: https://dramatiq.io/\n',
    'author': 'Étienne BERSAC',
    'author_email': None,
    'url': 'https://gitlab.com/dalibo/dramatiq-pg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
