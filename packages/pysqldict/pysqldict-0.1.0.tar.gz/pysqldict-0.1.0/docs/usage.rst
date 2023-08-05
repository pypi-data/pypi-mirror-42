=====
Usage
=====

To use pysqldict in a project::

	import pysqldict

	# Create a database instance
	db = pysqldict('settings.db')

	# Get table reference
	config = db.table('config')

	# Store data
	config.put({'key': 'domain', 'value': 'example.com'})
	config.put({'key': 'username', 'value': 'test_user_1', 'password_type': 'sha256'})
	config.put({'key': 'username', 'value': 'test_user_2', 'password_type': 'md5'})

	# Fetch one data
	config.get(key='domain')
	# {'_id': 1, 'key': 'domain', 'value': 'example.com'}

	# Fetch multiple data
	config.filter(key='username')
	# [{'_id': 2,
	#  'key': 'username',
	#  'value': 'test_user_1',
	#  'password_type': 'sha256'},
	# {'_id': 3, 'key': 'username', 'value': 'test_user_2', 'password_type': 'md5'}]

