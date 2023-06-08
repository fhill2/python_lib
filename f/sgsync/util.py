import os, errno
def symlink(source, target):
    if not os.path.lexists(target):
        try:
            os.symlink(source, target)
        except OSError as e:
            if e.errno == errno.ENOENT:
                os.makedirs(os.path.dirname(target), mode = 0o777, exist_ok=True)
                symlink(source, target)
            else:
                print("failed to create symlink: " + source + " --> " + target)
                exit()
        else:
            print("+ " + source + " --> " + target)
