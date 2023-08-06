import os

def get_dir_fname_suffix(path):
    dirname = os.path.dirname(path)
    basename = os.path.basename(path)
    if not '.' in basename:
        fname = basename
        suffix = None
    else:
        suffix = basename.split('.')[-1]
        fname = basename[:-len(suffix)]
    return dirname,fname,suffix

def add_tag(path,tag):
    dirname,fname,suffix = get_dir_fname_suffix(path)
    if suffix is not None:
        fname = fname+'tag.'+suffix
    else:
        fname = fname+'tag'
    return os.path.join(dirname,fname)

def add_prefix(path,prefix):
    dirname,fname,suffix = get_dir_fname_suffix(path)
    if suffix is not None:
        fname = prefix+fname+'.'+suffix
    else:
        fname = prefix+fname
    return os.path.join(dirname,fname)

def change_suffix(path,suffix):
    dirname,fname,_ = get_dir_fname_suffix(path)
    return os.path.join(dirname,fname+'.'+suffix)
