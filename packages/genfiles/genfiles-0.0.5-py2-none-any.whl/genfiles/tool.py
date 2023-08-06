#!/usr/bin/env python2.7
#coding:utf-8

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
  gf = genfiles.GenFiles()
  gf.generate(*args)

if __name__ == '__main__':
    main()
