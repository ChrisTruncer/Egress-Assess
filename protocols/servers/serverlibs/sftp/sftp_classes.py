import base64
import os
import paramiko
import tempfile
import threading
import time
from io import StringIO


class User(object):
    def __init__(self, username, password,
                 chroot=True, home=None, public_key=None):
        self.username = username
        self.password = password
        self.chroot = chroot
        self.public_key = public_key
        if type(self.public_key) in (str, str):
            bits = base64.decodebytes(self.public_key.key(' ')[1])
            msg = paramiko.Message(str(bits))
            key = paramiko.RSAKey(msg)
            self.public_key = key

        self.home = home
        if self.home is None:
            self.home = self.username


class SFTPHandle(paramiko.SFTPHandle):
    def __init__(self, flags=0, path=None):
        paramiko.SFTPHandle.__init__(self, flags)
        self.path = path
        if flags == 0:
            self.readfile = open(path, "r")
        else:
            self.writefile = open(path, "w")


class SvnSFTPHandle(SFTPHandle):
    def __init__(self, flags=0, path=None):
        paramiko.SFTPHandle.__init__(self, flags)
        self.path = path
        if flags == 0:
            self.readfile = open(path, "r")
        else:
            self.writefile = open(path, "w")

    def close(self):
        paramiko.SFTPHandle.close(self)

        writefile = getattr(self, 'writefile', None)
        if writefile is not None:
            writefile.close()
            os.system(f"svn add {self.path}")
            os.system(f"svn commit -m 'auto add' {self.path}")


class SimpleSftpServer(paramiko.SFTPServerInterface):
    def __init__(self, server, transport, fs_root, users, *largs, **kwargs):
        super().__init__(server, *largs, **kwargs)
        self.transport = transport
        self.root = fs_root
        self.user_name = self.transport.get_username()
        self.users = users

        if self.users[self.user_name].chroot:
            self.root = "{0}/{1}".format(self.root, self.users[self.user_name].home)

    def get_fs_path(self, sftp_path):
        real_path = "{0}/{1}".format(self.root, sftp_path)
        real_path = real_path.replace('//', '/')

        if not os.path.realpath(real_path).startswith(self.root):
            raise Exception("Invalid path")

        return real_path

    def open(self, path, flags, attr):
        real_path = self.get_fs_path(path)
        return SFTPHandle(flags, real_path)

    def list_folder(self, path):
        real_path = self.get_fs_path(path)
        rc = []
        for filename in os.listdir(real_path):
            full_name = ("{0}/{1}".format(real_path, filename)).replace("//", "/")
            rc.append(paramiko.SFTPAttributes.from_stat(os.stat(full_name), filename.replace(self.root, '')))
        return rc

    def stat(self, path):
        real_path = self.get_fs_path(path)
        return paramiko.SFTPAttributes.from_stat(os.stat(real_path), path)

    def lstat(self, path):
        real_path = self.get_fs_path(path)
        return paramiko.SFTPAttributes.from_stat(os.stat(real_path), path)

    def remove(self, path):
        real_path = self.get_fs_path(path)
        os.remove(real_path)
        return 0

    def rename(self, oldpath, newpath):
        real_oldpath = self.get_fs_path(oldpath)
        real_newpath = self.get_fs_path(newpath)
        os.rename(real_oldpath, real_newpath)
        return 0

    def mkdir(self, path, attr):
        real_path = self.get_fs_path(path)
        os.makedirs(real_path)
        return 0

    def rmdir(self, path):
        return

    def chattr(self, path, attr):
        return

    def readlink(self, path):
        return

    def symlink(self, target_path, path):
        return


class SubversionSftpServer(SimpleSftpServer):
    def __init__(self, *largs, **kwargs):
        SimpleSftpServer.__init__(self, *largs, **kwargs)

    def open(self, path, flags, attr):
        real_path = self.get_fs_path(path)
        return SvnSFTPHandle(flags, real_path)

    def remove(self, path):
        real_path = self.get_fs_path(path)
        os.system('svn del {}'.format(real_path))
        os.system("svn commit -m 'auto commit for {0}' {1}".format(self.user_name, real_path))
        return 0

    def rename(self, oldpath, newpath):
        real_oldpath = SimpleSftpServer.get_fs_path(self, oldpath)
        real_newpath = SimpleSftpServer.get_fs_path(self, newpath)
        os.system("svn mv {0} {1}".format(real_oldpath, real_newpath))
        os.system("svn commit -m 'auto commit for {0}' {1} {2}".format(self.user_name, real_oldpath, real_newpath))
        return 0


class IntegrationTestSftpServer(SimpleSftpServer):
    def __init__(self, *largs, **kwargs):
        SimpleSftpServer.__init__(self, *largs, **kwargs)

        tempdir = tempfile.mkdtemp()
        os.system(f"cp -r {self.root}/* {tempdir}")
        self.root = tempdir

    def session_ended(self):
        os.system(f"rm -rf {self.root}")


class SimpleSSHServer(paramiko.ServerInterface):
    def __init__(self, users):
        self.event = threading.Event()
        self.users = users
        self.authenticated_user = None

    def check_channel_request(self, kind, chanid):
        return paramiko.OPEN_SUCCEEDED

    def check_auth_password(self, username, password):
        if username in self.users:
            if self.users[username].password == password:
                return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        if username in self.users:
            u = self.users[username]
            if u.public_key is not None:
                if u.public_key.get_base64() == key.get_base64():
                    return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return 'password,publickey'

    def get_authenticated_user(self):
        return self.authenticated_user

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True


def accept_client(client, addr, root_dir, users, host_rsa_key, conf={}):
    usermap = {}
    for u in users:
        usermap[u.username] = u

    host_key_file = StringIO(host_rsa_key)
    host_key = paramiko.RSAKey(file_obj=host_key_file)
    transport = paramiko.Transport(client)
    transport.load_server_moduli()
    transport.add_server_key(host_key)

    if "sftp_implementation" in conf:
        mod_name, class_name = conf['sftp_implementation'].split(':')
        fromlist = None
        try:
            parent = mod_name[0:mod_name.rindex('.')]
            fromlist = [parent]
        except:
            pass
        mod = __import__(mod_name, fromlist=fromlist)
        impl = getattr(mod, class_name)

    else:
        impl = SimpleSftpServer
    transport.set_subsystem_handler("sftp", paramiko.SFTPServer, sftp_si=impl, transport=transport, fs_root=root_dir, users=usermap)

    server = SimpleSSHServer(users=usermap)
    transport.start_server(server=server)
    channel = transport.accept()
    while transport.is_active():
        time.sleep(3)

    username = server.get_authenticated_user()
    if username is not None:
        user = usermap[username]
        os.system("svn commit -m 'committing user session for {0}' {1}".format(username, root_dir + "/" + user.home))
