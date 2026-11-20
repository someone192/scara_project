from setuptools import find_packages, setup

package_name = 'scara_kinematics'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    package_data={'': ['py.typed']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Valerii Lebedintsev',
    maintainer_email='yavalera56@gmail.com',
    description='TODO: Package description',
    license='GPL-3.0-only',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'ik_node = scara_kinematics.ik_node:main'
        ],
    },
)
