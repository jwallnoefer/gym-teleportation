from setuptools import setup

setup(name='gym_teleportation',
      version='0.0.1',
      install_requires=['gym'],
      packages=['gym_teleportation'],
      package_dir={'gym_teleportation': 'mypkg'},
      package_data={'gym_teleportation': ['envs/teleportation']},)
