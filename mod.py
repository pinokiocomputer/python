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
  for package_name in dists:
    for dist_name in dists[package_name]:
      dict[dist_name] = {}
      # get package path
      try:
        meta = importlib_metadata.metadata(dist_name)
        files = importlib_metadata.files(dist_name)
        move = set()
        copy = set()
        for file in files:
          filepath = os.path.join(sitepackages_base, file)
          dirpath = os.path.abspath(os.path.dirname(filepath))
          try:
            relpath = Path(dirpath).relative_to(sitepackages_base)
            # site package handling
            chunks = str(relpath).split(os.sep)
            if len(chunks) > 1:
              folder = chunks[0]
              move.add(folder)
          except:
            # non site package handling
            # add the full file paths => so they can be copied
            copy.add(str(file))
        dict[dist_name]["version"] = meta["Version"]
        dict[dist_name]["copy"] = list(copy)
        dict[dist_name]["move"] = list(move)
      except Exception as error:
        print(f"#ERR {error}")
  return dict
