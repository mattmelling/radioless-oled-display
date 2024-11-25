from setuptools import setup, find_packages


setup(name='radioless-oled-display',
      version='1.0',
      description='Radioless display driver',
      packages=find_packages(),
      include_package_data=True,
      package_data={
          'radioless_oled_display': ['images/*.png']
      },
      install_requires=[
          'luma.core == 2.4.0',
          'luma.emulator',
          'luma.oled == 3.12.0',
          'pyftdi == 0.54.0',
          'pystrix',
          'importlib_resources == 4.1.0'
      ],
      entry_points={
          'console_scripts': [
              'radioless-oled-display=radioless_oled_display.cli:main'
          ]
      }
)
