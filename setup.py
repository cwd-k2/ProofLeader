import setuptools

setuptools.setup(
    name='ProofLeader_cwd-k2',
    version='3.0.0',
    entry_points={
        'console_scripts': [
            'proof_leader=proof_leader:main'
        ],
    },
    author='cwd-k2',
    url='https://github.com/cwd-k2/ProofLeader',
    python_requires='>=3.2',
)
