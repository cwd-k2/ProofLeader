import setuptools

setuptools.setup(
    name='ProofLeader_cwd-k2',
    entry_points={
        'console_scripts': [
            'proof_leader=proof_leader:main'
        ],
    },
    author='cwd-k2',
    python_requires='>=3.2',
)
