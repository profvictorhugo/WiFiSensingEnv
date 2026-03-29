from setuptools import setup
PACKAGE_NAME = 'csi'

setup(
    name=PACKAGE_NAME,
    version='0.0.1',
    packages=[PACKAGE_NAME],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + PACKAGE_NAME]),
        ('share/' + PACKAGE_NAME, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vitoria',
    maintainer_email='silva.lopes.vitoria@gmail.com',
    description='CSI',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'csi_publisher = csi.publisher_contador:main',
            'csi_subscriber = csi.subscriber_contador:main',
        ],
    },
)
