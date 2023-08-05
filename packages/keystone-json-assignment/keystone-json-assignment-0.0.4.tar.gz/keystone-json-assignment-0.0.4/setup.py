from setuptools import setup

setup(
    name='keystone-json-assignment',
    version='0.0.4',
    description='JSON Backend for the Keystone Assignment Driver',
    url='https://github.com/SUSE-Cloud/keystone-json-assignment',
    author='Colleen Murphy',
    author_email='colleen.murphy@suse.com',
    license='Apache-2.0',
    packages=['keystone_json_assignment'],
    entry_points={
        'keystone.assignment': ['json = keystone_json_assignment.json:Assignment'],
    }
)
