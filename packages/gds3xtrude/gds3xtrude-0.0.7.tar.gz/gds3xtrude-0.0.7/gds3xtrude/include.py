#
# Copyright (c) 2018 Thomas Kramer.
#
# This file is part of gds3xtrude
# (see https://teahub.io/miaou/gds3xtrude).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from .layer_operations import AbstractLayer
from typing import Tuple, Optional


def layer(idx: int,
          purpose: int = 0,
          color: Optional[Tuple[float, float, float]] = None) -> AbstractLayer:
    """ Get a handle to a layer by layer number.
    :param idx: GDS layer number or a string of the form '1/0'.
    :param purpose: GDS layer purpose.
    :param color: The color of the layer in the 3D model.
    :return: Handle to the layer.
    """

    # Allow idx to be a string like '1/0'.
    if isinstance(idx, str):
        s = idx.split('/', 2)
        a, b = s
        idx = int(a)
        purpose = int(b)

    return AbstractLayer(idx, purpose, color=color)
