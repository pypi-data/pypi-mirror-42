from setuptools import setup

setup(name='dotnetAddDlls',
    version='0.1',
    description='Add dlls to your dotnet core project',
    url='https://github.com/YotamShvartsun/dotnetAddDlls',
    author='Yotam Shvartsun',
    author_email='yotam.shvartsun@gmail.com',
    license='MIT',
    packages=['dotnetAddDlls'],
    entry_points={
        'console_scripts':['dotnet-add-dll=dotnetAddDlls:main']
    },
    data_files=[('templates', ['dotnetAddDlls/RefTemplate.xml'])]
)