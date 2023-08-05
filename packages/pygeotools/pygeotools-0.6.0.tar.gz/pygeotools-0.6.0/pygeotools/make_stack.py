#! /usr/bin/env python

#Generate stack from input rasters

import os
import sys
import argparse

import numpy as np
from pygeotools.lib import malib

#Hack to work around file open limit
#import resource
#resource.setrlimit(resource.RLIMIT_CORE,(resource.RLIM_INFINITY, resource.RLIM_INFINITY))

def getparser():
    parser = argparse.ArgumentParser(description='Utility to warp stacks of rasters to the same res/extent/proj')
    parser.add_argument('-tr', default='max', help='Output resolution (default: %(default)s)')
    parser.add_argument('-te', default='union', help='Output extent (default: %(default)s)')
    parser.add_argument('-t_srs', default='first', help='Output projection (default: %(default)s)')
    parser.add_argument('-outdir', default=None, help='Output directory')
    parser.add_argument('-stack_fn', default=None, help='Output filename')
    parser.add_argument('-min_dt_ptp', type=float, default=np.nan, help='Minimum number of days between first and last obs for trend calculation at each valid pixel')
    parser.add_argument('-min_n', type=int, default=2, help='Minimum number of obs for trend calculation at each valid pixel')
    parser.add_argument('-n_cpu', default=None, help='Number of parallel processes to use for robust trend calculation')
    parser.add_argument('--trend', dest='trend', action='store_true')
    parser.add_argument('--robust', dest='robust', action='store_true')
    parser.add_argument('--no-trend', dest='trend', action='store_false')
    parser.add_argument('--med', dest='med', action='store_true')
    parser.add_argument('--no-med', dest='med', action='store_false')
    parser.add_argument('--stats', dest='stats', action='store_true')
    parser.add_argument('--no-stats', dest='stats', action='store_false')
    parser.add_argument('--save', dest='save', action='store_true')
    parser.add_argument('--no-save', dest='save', action='store_false')
    parser.add_argument('--datestack', dest='datestack', action='store_true')
    parser.add_argument('--no-datestack', dest='datestack', action='store_false')
    parser.add_argument('--sort', dest='sort', action='store_true')
    parser.add_argument('--no-sort', dest='sort', action='store_false')
    parser.add_argument('src_fn_list', nargs='+', help='Input filenames (img1.tif img2.tif ...)')
    parser.set_defaults(trend=True, med=False, stats=True, save=True, datestack=True, sort=True)
    return parser

def main():
    parser = getparser()
    args = parser.parse_args()

    if args.stack_fn is not None:
        if os.path.exists(args.stack_fn):
            sys.exit("Found existing stack_fn: %s" % args.stack_fn)

    #Note: res and extent are passed directly to warplib.memwarp_multi_fn, so can be many types
    s = malib.DEMStack(fn_list=args.src_fn_list, stack_fn=args.stack_fn, outdir=args.outdir, \
            res=args.tr, extent=args.te, srs=args.t_srs, \
            trend=args.trend, robust=args.robust, n_thresh=args.min_n, min_dt_ptp=args.min_dt_ptp, n_cpu=args.n_cpu, \
            med=args.med, stats=args.stats, save=args.save, sort=args.sort, datestack=args.datestack)
    print(s.stack_fn)

if __name__ == '__main__':
    main()
