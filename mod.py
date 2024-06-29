import sys
import importlib
import importlib_metadata
from pathlib import Path
import os
# Get all the pip packages for the base path
def get(sitepackages_base):
  sys.path=[sitepackages_base]
  importlib.invalidate_caches()
  dists = importlib_metadata.packages_distributions()
  dict = {}
  # for every installed package, run the following logic:
  for package_name in dists:
    for dist_name in dists[package_name]:
      dict[dist_name] = {}

      # check if the distribution is installed from a custom repository
      try:
        origin = importlib_metadata.distribution(dist_name).origin
        print(f"origin = {origin}")
        if origin.url:
          dict[dist_name]["url"] = origin.url
          if origin.archive_info:
            dict[dist_name]["info"] = origin.archive_info
            # install from archive
            # example: https://github.com/pypa/pip/archive/1.3.1.zip
          elif origin.vcs_info:
            # install from repository
            # example: https://github.com/pypa/pip.git
            dict[dist_name]["info"] = origin.vcs_info
          elif origin.dir_info:
            # local
            dict[dist_name]["info"] = origin.dir_info
      except Exception as error:
        print(f"ERR1 {error}")

      # get package path
      try:
        # get the metadata for the package
        meta = importlib_metadata.metadata(dist_name)
        # get all files for the package
        files = importlib_metadata.files(dist_name)
        move = set()
        copy = set()
        # for each file in the package, get its parent folder, and 
        for file in files:
          filepath = os.path.join(sitepackages_base, file)
          dirpath = os.path.abspath(os.path.dirname(filepath))

          # if dirpath is a supath of sitepackages_base + "/" => move
          # otherwise => copy

          # [move]
          # if the dirpath (file's parent folder) starts with "lib/python3.10/site-packages/"
          # it means it's a package file. => move the package directory folder
          if os.path.abspath(dirpath).startswith(sitepackages_base + os.sep):
            relpath = Path(dirpath).relative_to(sitepackages_base)
            # site package handling
            chunks = str(relpath).split(os.sep)
            folder = chunks[0]
            move.add(folder)

          # [copy]
          # if the dirpath (file's parent folder) does NOT start with "lib/python3.10/site-packages/"
          # it means the file is in other paths such as "bin/accelerate", "include/..."
          # In this case need to copy the files since these files don't have version info specified on the file name
          # therefore just to be safe, copy those files to the drive so the exact required files are used
          else:
            # non site package handling
            # add the full file paths => so they can be copied
            copy.add(str(file))

        dict[dist_name]["version"] = meta["Version"]
        dict[dist_name]["copy"] = list(copy)
        dict[dist_name]["move"] = list(move)
      except Exception as error:
        print(f"#ERR2 {error}")
  return dict
