r"""Command-line tool to bslideshow

Usage::

    $ bs_footage /home/mivideo.mp4 foreground.mp4 /output/fout.mp4

"""
import sys
import genfiles

def main():
  args = []
  for i in range(2, len(sys.argv)):
    args.append(sys.argv[i])

  getattr(sys.modules[__name__], sys.argv[1])(args)

#args: templatePath, dataPath=None, outputPath=None
def generate (args):
  print("executing genfiles " + str(args))
  gf = genfiles.JinjaGenFiles()
  gf.generate(*args)

if __name__ == '__main__':
    main()
