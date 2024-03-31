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
          'luma.core',
          'luma.emulator',
          'luma.oled',
          'pystrix',
          'importlib_resources'
      ],
      entry_points={
          'console_scripts': [
              'radioless-oled-display=radioless_oled_display.cli:main'
          ]
      }
)
