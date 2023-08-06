import setuptools

with open('README.md', 'r') as f:
	description = f.read()

setuptools.setup(
	name='anna_tasks',
	version='1.0.1',
	author='Patrik Pihlstrom',
	author_email='patrik.pihlstrom@gmail.com',
	url='https://github.com/patrikpihlstrom/anna-tasks',
	description='anna task package',
	long_description=description,
	long_description_content_type='text/markdown',
	packages=['anna_tasks', 'anna_tasks.test', 'anna_tasks.test.iframe', 'anna_tasks.base',
	          'anna_tasks.base.checkout', 'anna_tasks.base.checkout.cart', 'anna_tasks.lillynails',
                  'anna_tasks.lillynails.customer', 'anna_tasks.lillynails.customer.login',
                  'anna_tasks.lillynails.checkout', 'anna_tasks.lillynails.checkout.cart', 'anna_tasks.lillynails.checkout.order']
)
