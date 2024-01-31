import pkg_resources
import platform
from pathlib import Path
import site
import sysconfig
import sys
import importlib
import importlib_metadata
import os

# Get all the pip packages for the base path
def list(sitepackages_base):
#  print(f"LIST {sitepackages_base}")
  sys.path=[sitepackages_base]
  importlib.invalidate_caches()

#  sys.path.insert(0, sitepackages_base)
  print(f"sys.path={sys.path}")
  print(f"sys.meta_path={sys.meta_path}")
  print(f"sys.path_hooks={sys.path_hooks}")
  #dists = importlib_metadata.packages_distributions()
  dists = importlib_metadata.packages_distributions()
  print(f"dists={dists}")
#  print(f"DISTS {dists}")

#  print(f"SYSPATH {sys.path}")
#  for key in sys.modules:
#    print(f"## {key}: {sys.modules[key]}")
#  print(f"sys.modules={sys.modules}")
  #print(f"BEFORE PATH: {sys.path}")
  #print(f"AFTER PATH: {sys.path}")
#  pkg_resources.working_set.add_entry(sitepackages_base)
  sitepackages_path = sysconfig.get_paths()["purelib"]
  dict = {}
#  packages = importlib.resources.files(package)
  for package_name in dists:
    print(f"package_name={package_name}")
    for dist_name in dists[package_name]:
      # get package path
      try:
        meta = importlib_metadata.metadata(dist_name)
        files = importlib_metadata.files(dist_name)

        for file in files:

          #if str(file).startswith("_"):
          if str(file).startswith("__pycache__"):
            continue
          if str(file).startswith("."):
            continue


          # if the resolved path
          abspath = os.path.join(sitepackages_base, file)
          is_child = Path(abspath).is_relative_to(sitepackages_base) and (sitepackages_base in abspath)
          if is_child:
            relative = str(file)
            chunks = relative.split(os.sep)
            if len(chunks) > 1:
              folder = chunks[0]
              package_path = str(os.path.join(sitepackages_base, folder))
              if not hasattr(dict, folder):
                dict[folder] = {}

              try:
                dict[folder]["version"] = meta["Version"]
              except:
                print('no version')
              dict[folder]["name"] = folder
              dict[folder]["path"] = package_path
      except Exception as error:
        print(f"#ERR {error}")
        # nothing

    # get dist path (only if there's a version)

  print(f"DICT={dict}")

  return dict
