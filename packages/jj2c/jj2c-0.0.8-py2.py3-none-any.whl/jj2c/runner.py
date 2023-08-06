import tempfile

CLOUD_FS = ['gs://', 's3://']


def is_cloud(src):
  if src[:4] in CLOUD_FS:
    return True
  return False


def gs_cp(src, dst):
  cmd = 'gsutil -m cp -r {src} {dst}'.format(src=src, dst=dst)


def s3_cp(src, dst):
  cmd = 's3 cp --recursive {src} {dst}'.format(src=src, dst=dst)


def s3_sync(src, dst):
  pass


class Runner(object):

  def __init__(self, src, dest):
    self.src = src
    self.dest = dest
    if is_cloud(self.src):
      pass
    self.actual_src = src

  def __enter__(self):
    self.temp_root = tempfile.mkdtemp()
    if not self.is_cloud(self.src):
      self.cloud_cp_to_local()

  def ensure_actual_src(self):
    self.cloud_src_localpath = os.path.join(self.temp_root, 'cloud_src')
    self.actual_src = os.path.join(self.cloud_src_localpath)

    if self.src.startswith('gs://'):
      gs_cp(self.src, self.actual_src)
    elif self.src.startswith('s3://'):
      s3_cp(self.src, self.actual_src)
