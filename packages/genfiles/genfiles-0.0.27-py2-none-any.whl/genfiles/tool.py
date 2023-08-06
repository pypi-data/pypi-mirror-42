r"""Command-line tool to bslideshow

Usage::

    $ bs_footage /home/mivideo.mp4 foreground.mp4 /output/fout.mp4

"""
import sys
import os
import tempfile
import genfiles
import shutil

def main():
  args = []
  for i in range(2, len(sys.argv)):
    args.append(sys.argv[i])

  getattr(sys.modules[__name__], sys.argv[1])(args)

#args: templatePath, dataPath=None, outputPath=None
def generate (args):
  #print("executing genfiles " + str(args))
  gf = genfiles.JinjaGenFiles()
  gf.generate(*args)

#args: type
def help (args):
  #print("executing help " + str(args))
  _show_help(*args)

def printFile (filePath):
  with open(filePath, 'r') as fin:
    print fin.read()

def printTemplate (name):
  filePath = os.path.join(os.path.join(os.path.dirname(__file__), 'templates'), name)
  print("")
  print(">>> template " + name + " (start)")
  printFile(filePath)
  print(">>> template " + name + " (end)")
  print("")

def copyTemplate (name, outDir):
  srcPath = os.path.join(os.path.join(os.path.dirname(__file__), 'templates'), name)
  dstPath = os.path.join(outDir, name)
  shutil.copyfile(srcPath, dstPath)

def _show_help (type=None):
  if type == 'base':
    printTemplate('data.hjson')
    printTemplate('header.txt')
    printTemplate('macros.txt')
    printTemplate('base.txt')
  elif type == 'inheritance':
    printTemplate('data.hjson')
    printTemplate('header.txt')
    printTemplate('parent.txt')
    printTemplate('child.txt')
  elif type == 'class':
    printTemplate('items.hjson')
    printTemplate('item.py')
    printTemplate('items.txt')
  elif type == 'data':
    printTemplate('data.hjson')
  elif type == 'test':
    cwd = os.getcwd()
    tmpDir = tempfile.mkdtemp(suffix='_genfiles', prefix='test_', dir=cwd)
    copyTemplate('base.txt', tmpDir)
    copyTemplate('child.txt', tmpDir)
    copyTemplate('data.hjson', tmpDir)
    copyTemplate('header.txt', tmpDir)
    copyTemplate('macros.txt', tmpDir)
    copyTemplate('parent.txt', tmpDir)
    copyTemplate('items.txt', tmpDir)
    copyTemplate('items.hjson', tmpDir)
    print("cd " + tmpDir)
    print("Examples of 'test/generate files':")
    print("$ gf_generate base.txt data.hjson")
    print("$ gf_generate base.txt data.hjson base.out")
    print("$ gf_generate child.txt data.hjson")
  else:
    print("options: base, inheritance, class, data, test.")
    print("- base: Show a template to learn the main stuffs.")
    print("- inheritance: Show some templates to learn the inheritance.")
    print("- class: Show an example of class object.")
    print("- data: Show an example of data file.")
    print("- test: Download templates to use in learning.")
    print("")
    print("Examples of 'generate files':")
    print("$ gf_generate template.ext1")
    print("$ gf_generate template.ext1 data.ext2")
    print("$ gf_generate template.ext1 data.ext2 output.ext3")

if __name__ == '__main__':
    main()
