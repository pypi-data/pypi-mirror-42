# -*- coding: utf-8 -*-
#
#    Copyright 2019 Ibai Roman
#
#    This file is part of BOlib.
#
#    BOlib is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    BOlib is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with BOlib. If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import scipy.optimize as spo

from .random_grid import RandomGrid
from .sequential_optimization import SequentialOptimization


class BayesianOptimization(SequentialOptimization):
    """

    """
    def __init__(self, model, fitting_method, validation, af, seed):
        """

        """

        self.orig_model = model
        self.model = None
        self.fitting_method = fitting_method
        self.validation = validation
        self.af = af

        self.af.set_opt_method(self)

        super(BayesianOptimization, self).__init__(seed)

        self.log['step_log'] = []

    def next_sample(self, x_t, y_t):
        """

        :param x_t:
        :type x_t:
        :param y_t:
        :type y_t:
        :return:
        :rtype:
        """

        fit_log = self.fitting_method.fit(
            model=self.orig_model,
            folds=self.validation.get_folds(self.data),
        )
        self.model = self.orig_model.get_posterior(self.data)

        # TODO Use better optimization methods
        optimization_method = RandomGrid(np.random.randint(10000))

        # Send next sample to Evaluate
        result = spo.minimize(
            self.af.evaluate,
            None,
            bounds=self.bounds,
            method=optimization_method.minimize,
            options = {
                'maxiter': 20000
            }
        )

        x_sel = result.x
        af_sel = result.fun

        return x_sel, {
            'x_sel': x_sel,
            'af_sel': af_sel,
            'fit_log': fit_log
        }
