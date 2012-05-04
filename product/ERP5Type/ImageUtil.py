#############################################################################
#
# Copyright (c) 2011 Nexedi SA and Contributors. All Rights Reserved.
#                    Rafael Monnerat <rafael@nexedi.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

import urllib2
from lxml import etree
from Products.ERP5.Document.Document import ConversionError

def getDataURI(url):
  try:
    data = urllib2.urlopen(url)
  except Exception, e:
    raise ConversionError("Error to transform url (%s) into data uri. ERROR = %s" % (url, Exception(e)))
  return 'data:%s;base64,%s' % (data.info()["content-type"],
                                data.read().encode("base64").replace('\n', ""))

def transformUrlToDataURI(content):
  if content is None or len(content) == 0:
    return content

  root = etree.fromstring(content)

  # Prevent namespace contains "None" included into svg by mistake
  namespace_dict = root.nsmap.copy()
  namespace_dict.pop(None, "discard")

  # Get all images which uses xlink:href
  image_list = root.xpath("//svg:image[@xlink:href]", namespaces=namespace_dict)
  xlink_href = "{%s}href" % namespace_dict.get("xlink", None)
  # Transform all images which uses url, into data URI
  for image in image_list:
    url_value = image.get(xlink_href)
    if url_value.startswith("http"):
      image.set(xlink_href, getDataURI(image.get(xlink_href)))

  return """<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n""" + \
         etree.tostring(root)
