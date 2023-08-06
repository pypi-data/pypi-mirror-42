# -*- coding: utf-8 -*-
#
#    Copyright 2019 Ibai Roman
#
#    This file is part of GPlib.
#
#    GPlib is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    GPlib is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with GPlib. If not, see <http://www.gnu.org/licenses/>.

import numpy as np

from .parameter import Parameter


class OptimizableParameter(Parameter):
    """

    """
    def __init__(self, name, transformation, default_value=1.0,
                 min_value=-np.inf, max_value=np.inf,
                 jitter_sd=0.1):
        """

        :param name:
        :type name:
        :param transformation:
        :type transformation:
        :param default_value:
        :type default_value:
        :param min_value:
        :type min_value:
        :param max_value:
        :type max_value:
        :param jitter_sd:
        :type jitter_sd:
        """

        super(OptimizableParameter, self).__init__(
            name, transformation, default_value
        )

        self.min_value = np.float64(min_value)
        self.max_value = np.float64(max_value)

        assert (np.all(self.min_value <= default_value) and
                np.all(default_value <= self.max_value)),\
            "{} is out of bounds".format(self.name)

        self.optimized_value = None

        self.jitter_sd = jitter_sd

    def set_param_values(self, params, optimizable_only=False, trans=False):
        """

        :param params:
        :type params:
        :param optimizable_only:
        :type optimizable_only:
        :param trans:
        :type trans:
        :return:
        :rtype:
        """

        super(OptimizableParameter, self).set_param_values(
            params, optimizable_only=optimizable_only, trans=trans
        )

        assert (np.all(self.min_value <= self.current_value) and
                np.all(self.current_value <= self.max_value)), \
            "{} is out of bounds".format(self.name)

    def set_params_to_default(self, optimizable_only=False):
        """

        :param optimizable_only:
        :type optimizable_only:
        :return:
        :rtype:
        """

        self.optimized_value = None

        super(OptimizableParameter, self).set_params_to_default(
            optimizable_only=optimizable_only
        )

    def set_params_at_random(self, trans=False):
        """

        :return:
        :rtype:
        """
        min_value = self.min_value
        max_value = self.max_value
        if trans:
            min_value = self.transformation.trans(min_value)
            max_value = self.transformation.trans(max_value)

        if self.optimized_value is not None:
            optimized_value = self.optimized_value
            if trans:
                optimized_value = self.transformation.trans(optimized_value)
            current_value = None
            while not (current_value is not None and
                       np.all(min_value < current_value) and
                       np.all(current_value < max_value)):
                current_value = optimized_value + \
                    np.array(
                        np.random.normal(
                            loc=0.0,
                            scale=self.jitter_sd,
                            size=self.dims
                        )
                    )
        else:
            current_value = np.array(np.random.uniform(
                min_value, max_value, self.dims
            ))

        self.set_param_values(current_value, trans=trans)

    def save_current_as_optimized(self):
        """

        :return:
        :rtype:
        """
        self.optimized_value = self.current_value

    def get_param_bounds(self, trans=False):
        """

        :param trans:
        :type trans:
        :return:
        :rtype:
        """

        min_value = self.min_value
        max_value = self.max_value

        if trans:
            min_value = self.transformation.trans(min_value)
            max_value = self.transformation.trans(max_value)

        return [(min_value, max_value)] * self.dims

    def set_min_value(self, min_value):
        """

        :param min_value:
        :type min_value:
        :return:
        :rtype:
        """
        self.min_value = min_value

    def set_max_value(self, max_value):
        """

        :param max_value:
        :type max_value:
        :return:
        :rtype:
        """
        self.max_value = max_value

    def grad_trans(self, df):
        """

        :param df:
        :type df:
        :return:
        :rtype:
        """

        return self.transformation.grad_trans(self.current_value, df)
