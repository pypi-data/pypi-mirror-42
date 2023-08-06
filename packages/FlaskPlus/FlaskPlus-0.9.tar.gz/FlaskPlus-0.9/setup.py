from setuptools import setup, find_packages

setup(
    name='FlaskPlus',
    version='0.9',
    url='https://github.com/Leon14451/flaskplus',
    project_urls=dict((
        ('Documentation', 'https://github.com/Leon14451/flaskplus'),
        ('Code', 'https://github.com/Leon14451/flaskplus')
    )),
    license='BSD',
    author='Leon',
    author_email='areuleon@gmail.com',
    description='Many powerful extensions for flask.',
    long_description='Many powerful extensions for flask, take code easy.',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    install_requires=[
        'flask>=1.0.2',
        'ujson>=1.35',
        'pymongo>=3.7.2'  # need ObjectId
    ],
    extras_require={
        'all': [
            'redis',
            'requests',
            'gunicorn',
            'minio'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points={
        'console_scripts': [
            'fps = flask_plus.starter.server:run',
            'fpd = flask_plus.starter.daemon:run',
        ],
    },
)
