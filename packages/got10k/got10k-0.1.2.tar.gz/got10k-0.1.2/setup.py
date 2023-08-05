from setuptools import setup, find_packages


setup(name='got10k',
      version='0.1.2',
      description='GOT-10k benchmark official API',
      author='Lianghua Huang',
      author_email='lianghua.huang.cs@gmail.com',
      url='https://github.com/got-10k/toolkit',
      license='MIT',
      install_requires=[
          'numpy', 'matplotlib', 'Pillow', 'Shapely', 'fire'],
      packages=find_packages(),
      include_package_data=True,
      keywords=[
          'GOT-10k',
          'Generic Object Tracking',
          'Benchmark',])
