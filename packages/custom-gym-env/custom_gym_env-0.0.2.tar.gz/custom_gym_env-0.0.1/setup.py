from setuptools import setup

setup(name='custom_gym_env',
      version='0.0.1',
      install_requires=['gym'],  # And any other dependencies foo needs
      packages=['custom_gym_envs']
)
