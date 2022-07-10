import os

from distutils import log

from glob import iglob
from shutil import copyfile, rmtree

from setuptools import find_packages, setup
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop


class copy_files_mixin(object):

    here = os.path.dirname(__file__)

    srcdir = os.path.join(here, "lightbox2", "dist")
    staticdir = os.path.join(here, "tw2", "jqplugins", "lightbox", "static")

    fileglobs = ('*/lightbox.*', 'images/*')

    def copy_files(self):
        log.info("Copying static files")

        if os.path.exists(self.staticdir):
            rmtree(self.staticdir)
        os.makedirs(self.staticdir)

        for globpat in self.fileglobs:
            for srcpath in iglob(os.path.join(self.srcdir, globpat)):
                dstpath = os.path.join(self.staticdir,
                                       srcpath[len(self.srcdir) + 1:])
                log.info("  {}\n    -> {}".format(srcpath, dstpath))
                dpath = os.path.dirname(dstpath)
                if not os.path.exists(dpath):
                    os.makedirs(os.path.dirname(dstpath))
                copyfile(srcpath, dstpath)


class my_build_py(build_py, copy_files_mixin):

    def run(self):
        if not self.dry_run:
            self.copy_files()
        build_py.run(self)


class my_develop(develop, copy_files_mixin):

    def install_for_development(self):
        self.copy_files()
        develop.install_for_development(self)

    def uninstall_link(self):
        develop.uninstall_link(self)

        log.info("Removing static files")
        rmtree(self.staticdir)


setup(
    name="tw2.jqplugins.lightbox",
    version="2.11.3",
    description="ToscaWidgets 2 wrapper for Lightbox",
    author="Nils Philippsen",
    author_email="nils@tiptoe.de",
    # url=
    # download_url=
    install_requires=["tw2.core>=2.0", "tw2.jquery>=2.0"],
    packages=find_packages(),
    namespace_packages=['tw2', 'tw2.jqplugins'],
    zip_safe=False,
    include_package_data=True,
    # test_suite="nose.collector"
    package_data={"tw2.jqplugins.lightbox": ["static/*"]},
    entry_points="""
        [tw2.widgets]
        widgets = tw2.jqplugins.lightbox
    """,
    keywords=["tw2.widgets"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Environment :: Web Environment :: ToscaWidgets",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Widget Sets",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    cmdclass={
        'build_py': my_build_py,
        'develop': my_develop,
    },
)
