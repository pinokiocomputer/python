import json
import sys
from tkinter import Tk, Toplevel, filedialog

"""
opts :=
  title             := <dialog title>
  type              := folder | file (default)
  cwd               := <cwd to open from>
  filetypes         := <file types to accept> (example:   [["Images", "*.png *.jpg *.jpeg"]] )
  multiple          := True | False (allow multiple)
  save              := True | False ('save as' dialog, which lets the user select a file name)
  initialfile       := In case of "save=True", set the default filename
  confirmoverwrite  := True | False (if set to true, will warn if the selected file name exists, for save=True type dialogs)
"""
def pick(opts):
    type_ = opts.get("type", "file")
    cwd = opts.get("cwd", "")
    title = opts.get("title", "Select")
    filetypes = opts.get("filetypes", [("All Files", "*.*")])
    multiple = opts.get("multiple", False)
    must_exist = opts.get("must_exist", True)
    save = opts.get("save", False)
    initialfile = opts.get("initialfile", "")
    confirmoverwrite = opts.get("confirmoverwrite", True)

    root = Tk()
    root.withdraw()

    top = Toplevel()
    top.attributes('-topmost', True)
    top.geometry("1x1+500+300")
    top.update()

    options = {
        "parent": top,
        "initialdir": cwd,
        "title": title
    }

    if type_ == "file":
        options["filetypes"] = filetypes
        if save:
            options["initialfile"] = initialfile
            options["confirmoverwrite"] = confirmoverwrite
            path = filedialog.asksaveasfilename(**options)
        elif multiple:
            path = filedialog.askopenfilenames(**options)
        else:
            path = filedialog.askopenfilename(**options)
    elif type_ == "folder":
        options["mustexist"] = must_exist
        path = filedialog.askdirectory(**options)
    else:
        raise ValueError(f"Unsupported type: {type_}")

    top.destroy()
    root.destroy()

    # Normalize return
    if isinstance(path, tuple):
        path = list(path)
    elif isinstance(path, str):
        path = [path] if path else []

    return path

def main():
    try:
        opts = json.load(sys.stdin)
        paths = pick(opts)
        print(json.dumps({"paths": paths}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
