#!python
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 03 14:54:34 2015

Muscle len consistency plot from Nexus. Automatically picks trials based on
Eclipse description and defined tags.

@author: Jussi (jnu@iki.fi)
"""

import logging
import argparse
from itertools import cycle

from gaitutils import (Plotter, cfg, register_gui_exception_handler,
                       normaldata, GaitDataError, sessionutils, nexus)

logger = logging.getLogger(__name__)


def do_plot(tags=None, age=None, show=True, make_pdf=True):

    tags = tags or cfg.eclipse.tags
    sessionpath = nexus.get_sessionpath()
    tagged_trials = sessionutils.get_c3ds(sessionpath, tags=tags,
                                          trial_type='dynamic')

    if not tagged_trials:
        raise GaitDataError('No marked trials found for current session')

    pl = Plotter()

    if age is not None:
        ndata = normaldata.normaldata_age(age)
        if ndata:
            pl.add_normaldata(ndata)

    pl.layout = cfg.layouts.overlay_musclelen

    linecolors = cfg.plot.overlay_colors
    ccolors = cycle(linecolors)

    for i, trialpath in enumerate(tagged_trials):
        logger.debug('plotting %s' % tagged_trials[i])
        pl.open_trial(tagged_trials[i])
        if i > len(linecolors):
            logger.warning('not enough colors for plot!')
        # only plot normaldata for last trial to speed up things
        plot_model_normaldata = (trialpath == tagged_trials[-1])
        pl.plot_trial(model_tracecolor=next(ccolors), linestyles_context=True,
                      toeoff_markers=False, add_zeroline=False, show=False,
                      maintitle='', superpose=True, sharex=False,
                      plot_model_normaldata=plot_model_normaldata)

    maintitle = ('Muscle length consistency plot, '
                 'session %s' % pl.trial.sessiondir)
    pl.set_title(maintitle)

    if show:
        pl.show()

    if make_pdf:
        pl.create_pdf('musclelen_consistency.pdf')

    return pl.fig


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--tags', metavar='p', type=str, nargs='+',
                        help='strings that must appear in trial '
                        'description or notes')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG)
    register_gui_exception_handler()
    do_plot(tags=args.tags)
