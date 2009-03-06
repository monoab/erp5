##############################################################################
#
# Copyright (c) 2008 Nexedi SA and Contributors. All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly adviced to contract a Free Software
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
# Foundation, Inc., 51 Franklin Street - Fifth Floor, Boston, MA 02110-1301, USA.
#
##############################################################################

from Products.ERP5.Document.MovementGroup import MovementGroup

class OrderMovementGroup(MovementGroup):
  """
  The purpose of MovementGroup is to define how movements are grouped,
  and how values are updated from simulation movements.

  This movement group is used to group movements that come from the same
  Order.
  """
  meta_type = 'ERP5 Movement Group'
  portal_type = 'Order Movement Group'

  def _getPropertyDict(self, movement, **kw):
    property_dict = {}
    order_relative_url = self._getOrderRelativeUrl(movement)
    property_dict['causality'] = order_relative_url
    return property_dict

  def test(self, movement, property_dict, **kw):
    if property_dict['causality'] in movement.getCausalityList():
      property_dict['causality'] = movement.getCausalityList()
      return True, property_dict
    else:
      return False, property_dict

  def _getOrderRelativeUrl(self, movement):
    if hasattr(movement, 'getRootAppliedRule'):
      # This is a simulation movement
      order_relative_url = movement.getRootAppliedRule().getCausality(
        portal_type=movement.getPortalOrderTypeList())
      if order_relative_url is None:
        # In some cases (ex. DeliveryRule), there is no order
        # we may consider a PackingList as the order in the OrderGroup
        order_relative_url = movement.getRootAppliedRule().getCausality(
          portal_type=movement.getPortalDeliveryTypeList())
    else:
      # This is a temp movement
      order_relative_url = None
    return order_relative_url
