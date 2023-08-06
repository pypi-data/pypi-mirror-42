# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from conu import S2IDockerImage, DockerBackend

# to make sure that temporary directory is cleaned
with DockerBackend():
    source = 'https://github.com/dbarnett/python-helloworld'
    image = S2IDockerImage("centos/python-35-centos7")
    extended_image = image.extend(source, "myapp")
    container = image.run_via_binary()

    container.stop()
    container.delete()
