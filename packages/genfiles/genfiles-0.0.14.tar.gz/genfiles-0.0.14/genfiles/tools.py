#!/usr/bin/env python2.7
#coding:utf-8

import hjson
import os
import jinja2
import codecs

class JinjaGenFiles:

  def __init__ (self):
    pass

  def generate (self, templatePath, dataPath=None, outputPath=None):
    cwd = os.getcwd()
    #print(str(cwd))

    if templatePath is not None and not os.path.isabs(templatePath):
      templatePath = os.path.join(cwd, templatePath)

    if dataPath is not None and not os.path.isabs(dataPath):
      dataPath = os.path.join(cwd, dataPath)

    if outputPath is not None and not os.path.isabs(outputPath):
      outputPath = os.path.join(cwd, outputPath)

    baseDir = os.path.dirname(templatePath)
    templateName = os.path.basename(templatePath)

    data = None
    if dataPath is not None:
      #print("load data path = " + dataPath)
      #data = dict(self.__loadObj__(dataPath))
      data = self.__loadObj__(dataPath)
      #print(str(data))

    file_loader = jinja2.FileSystemLoader(baseDir)
    env = jinja2.Environment(loader=file_loader)
    env.filters['myUpper'] = self.myUpper
    env.tests['verdadero'] = self.is_verdadero
    env.tests['falso'] = self.is_falso
    template = env.get_template(templateName)

    if outputPath is None:
      output = None
      if data is None:
        output = template.render()
      else:
        #print("render with data")
        output = template.render(data=data)
      print(output)
    else:
      stream = None
      if data is None:
        stream = template.stream()
      else:
        stream = template.stream(data=data)
      stream.dump(outputPath, encoding='utf-8')

  def __saveObj__ (self, path, obj):
    fp = codecs.open(path, mode='w', encoding='utf-8')
    hjson.dump(obj, fp)

  def __loadObj__ (self, path):
    result = None
    fp = codecs.open(path, mode='r', encoding='utf-8')
    result = hjson.load(fp)
    return result

  def myUpper(self, value, suffix='00'):
    suffix = suffix if suffix is not None else ''
    return value.upper() + suffix

  def is_verdadero(value):
    return True if value == 'True' else False

  def is_falso(value):
    return False if value == 'True' else True


def test():
  t = jinja2.Template("Hello {{ something }}!")
  print(t.render(something="World"))
  t = jinja2.Template("My favorite numbers: {% for n in range(1,10) %}{{n}} " "{% endfor %}")
  print(t.render())

def test2():
  file_loader = jinja2.FileSystemLoader('/media/jmramoss/ALMACEN/pypi/genfiles/genfiles')
  env = jinja2.Environment(loader=file_loader)
  template = env.get_template('hello.txt')
  output = template.render()
  print(output)

def test3():
  file_loader = jinja2.FileSystemLoader('/media/jmramoss/ALMACEN/pypi/genfiles/genfiles')
  env = jinja2.Environment(loader=file_loader)
  template = env.get_template('lamb.txt')
  output = template.render(name=u'Jesús')
  print(output)

def test4():
  person = {}
  person['name'] = u'Jesús'
  person['animal'] = u'murciélago'

  file_loader = jinja2.FileSystemLoader('/media/jmramoss/ALMACEN/pypi/genfiles/genfiles')
  env = jinja2.Environment(loader=file_loader)
  template = env.get_template('data.txt')
  output = template.render(data=person)
  print(output)

if True and __name__ == '__main__':
  tools = JinjaGenFiles()
  #tools.generate("hello.txt")
  #tools.generate("data.txt", dataPath="/media/jmramoss/ALMACEN/pypi/genfiles/genfiles/data.hjson")
  #tools.generate("data.txt", dataPath="/media/jmramoss/ALMACEN/pypi/genfiles/genfiles/data.hjson", outputPath="/media/jmramoss/ALMACEN/pypi/genfiles/genfiles/data.out")
  tools.generate("data.txt", dataPath="data.hjson", outputPath="data3.out")
  #test4()
  #print("HOLA2")
