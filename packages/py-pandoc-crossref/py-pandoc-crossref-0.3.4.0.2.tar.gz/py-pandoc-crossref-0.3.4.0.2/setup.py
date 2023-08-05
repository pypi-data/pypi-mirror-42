conda = False
# --------------------------
#
#
# --------------------------
from setuptools import setup
from setuptools.command.install import install
import os
import os.path as p
import platform
import shutil

src_dir = p.dirname(p.abspath(__file__))


def assert_64_bit_os():
    if not (platform.machine().endswith('64') or  # 64 bit OS if method is OK
            platform.architecture()[0] == '64bit'):  # 64 bit Python
        raise RuntimeError('Only 64bit OS is supported.')


# ------------------------------------------------------------------------------
# Custom settings:
# ------------------------------------------------------------------------------
assert_64_bit_os()
version = '0.3.4.0.2'
tmp = 'tmp'
spec = dict(
    Windows=dict(
        os='win', move=[('Library/bin', tmp)], version='0.3.4.0', build=1,
        hash='013acf9db3aab6a20e33ccc9b5a125c3269c71122382f906f3ed5d14bbb10c64'),
    Linux=dict(
        os='linux', move=[('bin', tmp)], version='0.3.4.0', build=1,
        hash='ea1afc3d864ebd955e875cf8dd61ca0f52674df367db4188303e0fb9ca5e41fb'),
    Darwin=dict(
        os='osx', move=[('bin', tmp)], version='0.3.4.0', build=1,
        hash='b474df3a8c44d68859efc911ff89fcba963eb4ba8a6674e6d5cfe4942c0bfc96'),
)[platform.system()]
URL = 'https://anaconda.org/conda-forge/pandoc-crossref/{version}/download/{os}-64/pandoc-crossref-{version}-{build}.tar.bz2'.format(**spec)


class PostInstallCommand(install):
    def run(self):
        excract_tar_and_move_files(url=URL, **spec)
        move_contents(
            from_=p.join(src_dir, tmp),
            to=self.install_scripts,
            set_exec=True)
        install.run(self)

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


def move_contents(from_, to, set_exec=False):
    import stat
    os.makedirs(to, exist_ok=True)
    for file in os.listdir(from_):
        to_file = p.join(to, file)
        shutil.move(p.join(from_, file),
                    to_file if p.isfile(to_file) else to)
        if p.isfile(to_file) and set_exec:
            if os.name != 'nt':
                st = os.stat(to_file)
                os.chmod(to_file, st.st_mode | stat.S_IEXEC)


def sha256(filename):
    """ https://stackoverflow.com/a/44873382/9071377 """
    import hashlib
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


def excract_tar_and_move_files(url, hash, move, **kwargs):
    """
    Moves relative to the setup.py dir. Can download more packages
    if the target archive contains setup.py

    * ``url`` should be of the form z/name.x.y.gz
      (gz, bz2 or other suffix supported by the tarfile module).
    * ``move`` contains pairs of dirs where to move contents.
      First dir is in the extracted archive,
      second dir is in the same folder as setup.py
    """
    import sys
    import tarfile
    from subprocess import call, run, PIPE
    import tempfile

    dirpath = tempfile.mkdtemp()
    cwd = os.getcwd()
    os.chdir(dirpath)

    call([sys.executable, "-m", "pip", "download", url], stdout=PIPE, stderr=PIPE)
    filename = url.split('/')[-1]
    ext = p.splitext(filename)[1][1:]
    if sha256(filename) != hash:
        raise RuntimeError(f'SHA256 hash does not match for {filename}')
    with tarfile.open(filename, f"r:{ext}") as tar:
        tar.extractall()

    for from_, to in move:
        from_ = p.abspath(p.normpath(from_))
        to = p.normpath(p.join(src_dir, to))
        os.makedirs(to, exist_ok=True)
        for s in os.listdir(from_):
            shutil.move(p.join(from_, s), to)
    os.chdir(cwd)
    shutil.rmtree(dirpath)


setup(
    name='py-pandoc-crossref',
    version=version,
    python_requires='>=3.6',
    description='pandoc-crossref in pip and conda',
    url='https://github.com/kiwi0fruit/py-pandoc-crossref',
    author='kiwi0fruit',
    author_email='peter.zagubisalo@gmail.com',
    license='GPLv2+',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=['py-pandoc>=2.5,<2.6.1'],
    **(dict(
        cmdclass={'install': PostInstallCommand}
    ) if not conda else {})
)
