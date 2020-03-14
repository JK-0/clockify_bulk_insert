from setuptools import setup

setup(
    name="clockify-bulk-insert",
    version="1.0",
    py_modules=["clockify"],
    include_package_data=True,
    install_requires=[
        "click",
        # Colorama is only required for Windows.
        "colorama",
        "helium",
        "pyfiglet",
        "PyInquirer",
        "six",
        "termcolor"
    ],
    entry_points="""
        [console_scripts]
        clockify=clockify:cli
    """,
)
