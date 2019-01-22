from __future__ import print_function

import Quartz
import CoreFoundation
import os

def write_cgimage(path, image):
  imurl = CoreFoundation.CFURLCreateWithFileSystemPath(
    CoreFoundation.kCFAllocatorDefault,
    (path),
    CoreFoundation.kCFURLPOSIXPathStyle,
    False
  )
  dest = Quartz.CGImageDestinationCreateWithURL(imurl, 'public.png', 1, None)
  Quartz.CGImageDestinationAddImage(dest, image, None)
  Quartz.CGImageDestinationFinalize(dest)
  print("wrote " + path)


windows = Quartz.CGWindowListCreateDescriptionFromArray(
  Quartz.CGWindowListCreate(Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID)
)
chromeWindows = [
  w
  for w in windows
  if w['kCGWindowOwnerName'] == u'Google Chrome'
  and w['kCGWindowBounds']['Height'] != 22
  and (('kCGWindowName' not in w) or (w['kCGWindowName'] != 'Focus Proxy'))
]
print(repr(chromeWindows))

for w in chromeWindows:
  wid = w['kCGWindowNumber']
  path = str(wid) + '.png'
  im = Quartz.CGWindowListCreateImageFromArray(Quartz.CGRectNull, [wid], Quartz.kCGWindowImageDefault)
  write_cgimage(path, im)

comp = Quartz.CGWindowListCreateImageFromArray(
  Quartz.CGRectNull,
  [w['kCGWindowNumber'] for w in chromeWindows],
  Quartz.kCGWindowImageDefault
)
write_cgimage('comp.png', comp)