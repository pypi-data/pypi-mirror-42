#!usr/bin/env python


from distutils.core import setup, Extension


privacy_admis2019_module = Extension('_privacy_admis2019', sources=['privacy_wrap.cxx', 'privacy.cpp'], )


setup(
    name='privacy_admis2019',# module name
    version='1.0',
    author="wukai",
    author_email = "2365388286@qq.com",
    url = "http://wukai.name",
    description = """privacy-preserving-algorithm""",
    ext_modules = [privacy_admis2019_module],
    py_modules=['privacy_admis2019']# python file
)
