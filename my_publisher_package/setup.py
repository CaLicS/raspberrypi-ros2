from setuptools import setup

package_name = 'my_publisher_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='your_email@example.com',
    description='A ROS2 package that publishes topics',
    license='License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'publisher = my_publisher_package.pub:main',  # main() 함수가 publisher.py에 있어야 함
        ],
    },
)
