#! /usr/bin/env python

#Todo
#Better outlier removal
#Check Nuth and Kaab bin median
#Implement check for empty diff

import sys
import os
import argparse
import subprocess

from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt

from pygeotools.lib import iolib, malib, geolib, warplib, filtlib

from demcoreg import coreglib, dem_mask

from imview.lib import pltlib

def get_mask(ds, mask_list, dem_fn=None):
    #This returns True (1) for areas to mask, False (0) for valid static surfaces
    static_mask = dem_mask.get_mask(ds, mask_list, dem_fn, writeout=False)
    #return ~(static_mask)
    return static_mask

def compute_offset(ref_dem_ds, src_dem_ds, src_dem_fn, mode='nuth', remove_outliers=True, max_offset=100, \
        max_dz=50, slope_lim=(0.1, 40), mask_list=['glaciers',], plot=True):
    #Make sure the input datasets have the same resolution/extent
    #Use projection of source DEM
    ref_dem_clip_ds, src_dem_clip_ds = warplib.memwarp_multi([ref_dem_ds, src_dem_ds], \
            res='max', extent='intersection', t_srs=src_dem_ds, r='cubic')

    #Compute size of NCC and SAD search window in pixels
    res = float(geolib.get_res(ref_dem_clip_ds, square=True)[0])
    max_offset_px = (max_offset/res) + 1
    #print(max_offset_px)
    pad = (int(max_offset_px), int(max_offset_px))

    #This will be updated geotransform for src_dem
    src_dem_gt = np.array(src_dem_clip_ds.GetGeoTransform())

    #Load the arrays
    ref_dem = iolib.ds_getma(ref_dem_clip_ds, 1)
    src_dem = iolib.ds_getma(src_dem_clip_ds, 1)

    print("Elevation difference stats for uncorrected input DEMs (src - ref)")
    diff_euler = src_dem - ref_dem

    static_mask = get_mask(src_dem_clip_ds, mask_list, src_dem_fn)
    diff_euler = np.ma.array(diff_euler, mask=static_mask)

    if diff_euler.count() == 0:
        sys.exit("No overlapping, unmasked pixels shared between input DEMs")

    #This needs further testing
    if remove_outliers:
        print("Removing outliers")
        print("Initial pixel count:")
        print(diff_euler.count())

        print("Absolute dz filter: %0.2f" % max_dz)
        #Absolute dz filter
        diff_euler = np.ma.masked_greater(diff_euler, max_dz)
        print(diff_euler.count())

        #Outlier dz filter
        f = 3
        nmad, med = malib.mad(diff_euler, return_med=True)
        rmin = med - f*nmad
        rmax = med + f*nmad
        print("3-sigma filter: %0.2f - %0.2f" % (rmin, rmax))
        diff_euler = np.ma.masked_outside(diff_euler, rmin, rmax)
        print(diff_euler.count())

        #Should also apply to original ref_dem and src_dem for sad and ncc

    #Generate slope map
    #Want to use higher quality DEM, should determine automatically from original res/count
    #slope = geolib.gdaldem_mem_ds(ref_dem_clip_ds, processing='slope', returnma=True, computeEdges=False)
    slope = geolib.gdaldem_mem_ds(src_dem_clip_ds, processing='slope', returnma=True, computeEdges=False)

    #slope_stats = malib.print_stats(slope)
    #Remove extreme slopes
    print("Slope filter: %0.2f - %0.2f" % slope_lim)
    print("Initial count: %i" % slope.count()) 
    slope = filtlib.range_fltr(slope, slope_lim) 
    print(slope.count())

    print("Computing aspect")
    #aspect = geolib.gdaldem_mem_ds(ref_dem_clip_ds, processing='aspect', returnma=True, computeEdges=False)
    aspect = geolib.gdaldem_mem_ds(src_dem_clip_ds, processing='aspect', returnma=True, computeEdges=False)

    ref_dem_clip_ds = None
    src_dem_clip_ds = None

    #Apply slope filter to diff_euler
    #Note that we combine masks from diff_euler and slope in coreglib
    diff_euler = np.ma.array(diff_euler, mask=np.ma.getmaskarray(slope))

    #Get final mask after filtering
    static_mask = np.ma.getmaskarray(diff_euler)

    #Compute stats for new masked difference map
    print("Filtered difference map")
    diff_stats = malib.print_stats(diff_euler)
    dz = diff_stats[5]

    print("Computing sub-pixel offset between DEMs using mode: %s" % mode)

    #By default, don't create output figure
    fig = None

    #Default horizntal shift is (0,0)
    dx = 0
    dy = 0

    #Sum of absolute differences
    if mode == "sad":
        ref_dem = np.ma.array(ref_dem, mask=static_mask)
        src_dem = np.ma.array(src_dem, mask=static_mask)
        m, int_offset, sp_offset = coreglib.compute_offset_sad(ref_dem, src_dem, pad=pad)
        #Geotransform has negative y resolution, so don't need negative sign
        #np array is positive down
        #GDAL coordinates are positive up
        dx = sp_offset[1]*src_dem_gt[1]
        dy = sp_offset[0]*src_dem_gt[5]
    #Normalized cross-correlation of clipped, overlapping areas
    elif mode == "ncc":
        ref_dem = np.ma.array(ref_dem, mask=static_mask)
        src_dem = np.ma.array(src_dem, mask=static_mask)
        m, int_offset, sp_offset, fig = coreglib.compute_offset_ncc(ref_dem, src_dem, \
                pad=pad, prefilter=False, plot=plot)
        dx = sp_offset[1]*src_dem_gt[1]
        dy = sp_offset[0]*src_dem_gt[5]
    #Nuth and Kaab (2011)
    elif mode == "nuth":
        #Compute relationship between elevation difference, slope and aspect
        fit_param, fig = coreglib.compute_offset_nuth(diff_euler, slope, aspect, plot=plot)
        if fit_param is None:
            print("Failed to calculate horizontal shift")
        else:
            #fit_param[0] is magnitude of shift vector
            #fit_param[1] is direction of shift vector
            #fit_param[2] is mean bias divided by tangent of mean slope
            #print(fit_param)
            dx = fit_param[0]*np.sin(np.deg2rad(fit_param[1]))
            dy = fit_param[0]*np.cos(np.deg2rad(fit_param[1]))
            med_slope = malib.fast_median(slope)
            nuth_dz = fit_param[2]*np.tan(np.deg2rad(med_slope))
            print('Median dz: %0.2f\nNuth dz: %0.2f' % (dz, nuth_dz))
            #dz = nuth_dz
    elif mode == "all":
        print("Not yet implemented")
        #Want to compare all methods, average offsets
        #m, int_offset, sp_offset = coreglib.compute_offset_sad(ref_dem, src_dem)
        #m, int_offset, sp_offset = coreglib.compute_offset_ncc(ref_dem, src_dem)
    elif mode == "none":
        print("Skipping alignment, writing out DEM with median bias over static surfaces removed")
        dst_fn = outprefix+'_med%0.1f.tif' % dz
        iolib.writeGTiff(src_dem_orig + dz, dst_fn, src_dem_ds)
        sys.exit()
    #Note: minus signs here since we are computing dz=(src-ref), but adjusting src
    return -dx, -dy, -dz, static_mask, fig

def getparser():
    parser = argparse.ArgumentParser(description="Perform DEM co-registration using multiple algorithms", \
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('ref_fn', type=str, help='Reference DEM filename')
    parser.add_argument('src_fn', type=str, help='Source DEM filename to be shifted')
    parser.add_argument('-mode', type=str, default='nuth', choices=['ncc', 'sad', 'nuth', 'none'], \
            help='Type of co-registration to use')
    parser.add_argument('-mask_list', nargs='+', type=str, default=['glaciers',], choices=dem_mask.mask_choices, \
            help='Define masks to use to limit reference surfaces for co-registration')
    parser.add_argument('-tiltcorr', action='store_true', \
            help='After preliminary translation, fit plane to residual elevation offsets and remove')
    parser.add_argument('-tol', type=float, default=0.02, \
            help='When iterative translation magnitude is below this tolerance (meters), break and write out corrected DEM')
    parser.add_argument('-max_offset', type=float, default=100, \
            help='Maximum expected horizontal offset in meters')
    parser.add_argument('-max_dz', type=float, default=100, \
            help='Maximum expected vertical offset in meters, used to filter outliers')
    parser.add_argument('-slope_lim', type=float, nargs=2, default=(0.1, 40), \
            help='Minimum and maximum surface slope limits to consider')
    parser.add_argument('-max_iter', type=int, default=20, \
            help='Maximum number of iterations, if tol is not reached')
    parser.add_argument('-outdir', default=None, help='Output directory')
    return parser

#Defined a second main to allow recursion with new arguments for second run
#Likely a cleaner strategy for this
def main2(args):
    #Should check that files exist
    ref_dem_fn = args.ref_fn
    src_dem_fn = args.src_fn

    mode = args.mode
    mask_list = args.mask_list
    max_offset = args.max_offset
    max_dz = args.max_dz
    slope_lim = args.slope_lim
    tiltcorr = args.tiltcorr

    #These are tolerances (in meters) to stop iteration
    tol = args.tol
    min_dx = tol
    min_dy = tol
    min_dz = tol

    #Maximum number of iterations
    max_n = args.max_iter

    outdir = args.outdir
    if outdir is None:
        #outdir = os.path.splitext(src_dem_fn)[0] + '_dem_align_lt1.5m_err'
        outdir = os.path.splitext(src_dem_fn)[0] + '_dem_align'

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    outprefix = '%s_%s' % (os.path.splitext(os.path.split(src_dem_fn)[-1])[0], \
            os.path.splitext(os.path.split(ref_dem_fn)[-1])[0])
    outprefix = os.path.join(outdir, outprefix)

    print("\nReference: %s" % ref_dem_fn)
    print("Source: %s" % src_dem_fn)
    print("Mode: %s" % mode)
    print("Output: %s\n" % outprefix)

    src_dem_ds = gdal.Open(src_dem_fn)
    #Create a copy to be updated in place
    #src_dem_ds_align = iolib.mem_drv.CreateCopy('', src_dem_ds, 0)
    #This is another approach that duplicates CreateCopy functionality
    ##src_dem_ds_align = geolib.mem_ds_copy(src_dem_ds)

    #Get local cartesian coordinate system
    #local_srs = geolib.localortho_ds(src_dem_ds)
    local_srs = geolib.localtmerc_ds(src_dem_ds)
    #local_srs = geolib.ds_get_srs(src_dem_ds)

    src_dem_ds_align = warplib.memwarp_multi_fn([src_dem_fn,], t_srs=local_srs, r='cubic')[0]

    src_dem_ds = None
    
    #Resample to match "source" DEM
    ref_dem_ds = warplib.memwarp_multi_fn([ref_dem_fn,], res=src_dem_ds_align, extent=src_dem_ds_align, t_srs=local_srs, r='cubic')[0]
    #ref_dem_ds = gdal.Open(ref_dem_fn) 

    #Iteration number
    n = 1
    #Cumulative offsets
    dx_total = 0
    dy_total = 0
    dz_total = 0

    #Now iteratively update geotransform and vertical shift
    while True:
        print("*** Iteration %i ***" % n)
        dx, dy, dz, static_mask, fig = compute_offset(ref_dem_ds, src_dem_ds_align, src_dem_fn, mode, max_offset, \
                mask_list=mask_list, max_dz=max_dz, slope_lim=slope_lim, plot=True)
        xyz_shift_str_iter = "dx=%+0.2fm, dy=%+0.2fm, dz=%+0.2fm" % (dx, dy, dz)
        print("Incremental offset: %s" % xyz_shift_str_iter)

        #Should make an animation of this converging
        if n == 1: 
            static_mask_orig = static_mask
            if fig is not None:
                dst_fn = outprefix + '_%s_iter%02i_plot.png' % (mode, n)
                print("Writing offset plot: %s" % dst_fn)
                fig.gca().set_title(xyz_shift_str_iter)
                fig.savefig(dst_fn, dpi=300)

        #Apply the horizontal shift to the original dataset
        src_dem_ds_align = coreglib.apply_xy_shift(src_dem_ds_align, dx, dy, createcopy=False)
        #Should 
        src_dem_ds_align = coreglib.apply_z_shift(src_dem_ds_align, dz, createcopy=False)

        dx_total += dx
        dy_total += dy
        dz_total += dz
        print("Cumulative offset: dx=%+0.2fm, dy=%+0.2fm, dz=%+0.2fm" % (dx_total, dy_total, dz_total))

        n += 1
        print("\n")
        #If magnitude of shift in all directions is less than tol
        #if n > max_n or (abs(dx) <= min_dx and abs(dy) <= min_dy and abs(dz) <= min_dz):
        #If magnitude of shift is less than tol
        dm = np.sqrt(dx**2 + dy**2 + dz**2)
        if n > max_n or dm < tol:
            if fig is not None:
                dst_fn = outprefix + '_%s_iter%02i_plot.png' % (mode, n)
                print("Writing offset plot: %s" % dst_fn)
                fig.gca().set_title(xyz_shift_str_iter)
                fig.savefig(dst_fn, dpi=300)
            break

    #String to append to output filenames
    xyz_shift_str_cum = '_%s_x%+0.2f_y%+0.2f_z%+0.2f' % (mode, dx_total, dy_total, dz_total)
    if tiltcorr:
        xyz_shift_str_cum += "_tiltcorr"

    #Compute original elevation difference
    if True:
        src_dem_ds = gdal.Open(src_dem_fn)
        ref_dem_clip_ds, src_dem_clip_ds = warplib.memwarp_multi([ref_dem_ds, src_dem_ds], \
                res='max', extent='intersection', t_srs=local_srs, r='cubic')
        src_dem_ds = None
        ref_dem_orig = iolib.ds_getma(ref_dem_clip_ds)
        src_dem_orig = iolib.ds_getma(src_dem_clip_ds)
        #Needed for plotting
        ref_dem_hs = geolib.gdaldem_mem_ds(ref_dem_clip_ds, processing='hillshade', returnma=True, computeEdges=True)
        src_dem_hs = geolib.gdaldem_mem_ds(src_dem_clip_ds, processing='hillshade', returnma=True, computeEdges=True)
        res = float(geolib.get_res(ref_dem_clip_ds, square=True)[0])
        diff_euler_orig = src_dem_orig - ref_dem_orig
        #Only compute stats over valid surfaces
        static_mask_orig = get_mask(src_dem_clip_ds, mask_list, src_dem_fn)
        #Note: this doesn't include outlier removal or slope mask!
        static_mask_orig = np.logical_or(np.ma.getmaskarray(diff_euler_orig), static_mask_orig)
        #For some reason, ASTER DEM diff have a spike near the 0 bin, could be an issue with masking?
        diff_euler_orig_compressed = diff_euler_orig[~static_mask_orig].compressed()
        diff_euler_orig_stats = np.array(malib.print_stats(diff_euler_orig_compressed))

        #Write out original eulerian difference map
        print("Writing out original euler difference map for common intersection before alignment")
        orig_eul_fn = outprefix + '_orig_dz_eul.tif'
        iolib.writeGTiff(diff_euler_orig, orig_eul_fn, ref_dem_clip_ds)
        src_dem_clip_ds = None
        ref_dem_clip_ds = None

    #Compute final elevation difference
    if True:
        ref_dem_clip_ds_align, src_dem_clip_ds_align = warplib.memwarp_multi([ref_dem_ds, src_dem_ds_align], \
                res='max', extent='intersection', t_srs=local_srs, r='cubic')
        ref_dem_align = iolib.ds_getma(ref_dem_clip_ds_align, 1)
        src_dem_align = iolib.ds_getma(src_dem_clip_ds_align, 1)
        #Need this for scalebar plot
        #res = float(geolib.get_res(src_dem_clip_ds_align, square=True)[0])
        diff_euler_align = src_dem_align - ref_dem_align
        src_dem_align = None
        ref_dem_align = None
        #Get updated, final mask
        static_mask_final = get_mask(src_dem_clip_ds_align, mask_list, src_dem_fn)
        src_dem_clip_ds_align = None
        static_mask_final = np.logical_or(np.ma.getmaskarray(diff_euler_align), static_mask_final)
        diff_euler_align_compressed = diff_euler_align[~static_mask_final].compressed()
        diff_euler_align_stats = np.array(malib.print_stats(diff_euler_align_compressed))

        #Fit plane to residuals and remove
        #Compute higher-order fits?
        #Could also attempt to model along-track and cross-track artifacts
        if tiltcorr:
            print("Applying planar tilt correction")
            gt = ref_dem_clip_ds_align.GetGeoTransform()
            #Need to apply the mask here, so we're only fitting over static surfaces
            #Note that the origmask=False will compute vals for all x and y indices, which is what we want
            #Should offer option for polynomial of arbitrary order
            #Also, want a better robust fit - maybe throw out more outliers
            vals, resid, coeff = geolib.ma_fitplane(np.ma.array(diff_euler_align, mask=static_mask_final), \
                    gt, perc=(12.5, 87.5), origmask=False)
            #Remove planar offset from difference map
            diff_euler_align -= vals
            #Remove planar offset from aligned src_dem
            #Note: dimensions of ds and vals will be different as vals are computed for clipped intersection
            #Recompute planar offset for src_dem_ds_align extent
            xgrid, ygrid = geolib.get_xy_grids(src_dem_ds_align)
            vals = coeff[0]*xgrid + coeff[1]*ygrid + coeff[2]
            src_dem_ds_align = coreglib.apply_z_shift(src_dem_ds_align, -vals, createcopy=False)
            diff_euler_align_compressed = diff_euler_align[~static_mask_final].compressed()
            diff_euler_align_stats = np.array(malib.print_stats(diff_euler_align_compressed))
            if True:
                print("Creating plot of planar correction")
                fig, ax = plt.subplots(figsize=(6, 6))
                fitplane_clim = malib.calcperc(vals, (2,98))
                im = ax.imshow(vals, cmap='cpt_rainbow', clim=fitplane_clim)
                pltlib.add_scalebar(ax, res=res)
                pltlib.hide_ticks(ax)
                pltlib.add_cbar(ax, im, arr=vals, clim=fitplane_clim, label='Fit plane residuals (m)')
                fig.tight_layout()
                tiltcorr_fig_fn = outprefix + '%s_align_dz_eul_fitplane.png' % xyz_shift_str_cum
                print("Writing out figure: %s" % tiltcorr_fig_fn)
                fig.savefig(tiltcorr_fig_fn, dpi=300)

        #Write out aligned eulerian difference map for clipped extent with vertial offset removed
        align_eul_fn = outprefix + '%s_align_dz_eul.tif' % xyz_shift_str_cum
        print("Writing out aligned difference map with median vertical offset removed")
        iolib.writeGTiff(diff_euler_align, align_eul_fn, ref_dem_clip_ds_align)
        ref_dem_clip_ds_align = None

    #Write out aligned dem_2 with vertial offset removed
    if True:
        align_fn = outprefix + '%s_align.tif' % xyz_shift_str_cum
        print("Writing out shifted src_dem with median vertical offset removed: %s" % align_fn)
        #Might be cleaner way to write out MEM ds directly to disk
        src_dem_align = iolib.ds_getma(src_dem_ds_align)
        iolib.writeGTiff(src_dem_align, align_fn, src_dem_ds_align)
        src_dem_align = None
        src_dem_ds_align = None

    #Create output plot
    if True:
        print("Creating final plot")
        f, axa = plt.subplots(2, 3, figsize=(11, 8.5))
        for ax in axa.ravel()[:-1]:
            ax.set_facecolor('k')
            pltlib.hide_ticks(ax)
        dem_clim = malib.calcperc(ref_dem_orig, (2,98))
        axa[0,0].imshow(ref_dem_hs, cmap='gray')
        im = axa[0,0].imshow(ref_dem_orig, cmap='cpt_rainbow', clim=dem_clim, alpha=0.6)
        pltlib.add_cbar(axa[0,0], im, arr=ref_dem_orig, clim=dem_clim, label=None)
        pltlib.add_scalebar(axa[0,0], res=res)
        axa[0,0].set_title('Reference DEM')
        axa[0,1].imshow(src_dem_hs, cmap='gray')
        im = axa[0,1].imshow(src_dem_orig, cmap='cpt_rainbow', clim=dem_clim, alpha=0.6)
        pltlib.add_cbar(axa[0,1], im, arr=src_dem_orig, clim=dem_clim, label=None)
        axa[0,1].set_title('Source DEM')
        #axa[0,2].imshow(~static_mask_orig, clim=(0,1), cmap='gray')
        axa[0,2].imshow(~static_mask, clim=(0,1), cmap='gray')
        axa[0,2].set_title('Surfaces for co-registration')
        dz_clim = malib.calcperc_sym(diff_euler_orig_compressed, (5, 95))
        im = axa[1,0].imshow(diff_euler_orig, cmap='RdBu', clim=dz_clim)
        pltlib.add_cbar(axa[1,0], im, arr=diff_euler_orig, clim=dz_clim, label=None)
        axa[1,0].set_title('Elev. Diff. Before (m)')
        im = axa[1,1].imshow(diff_euler_align, cmap='RdBu', clim=dz_clim)
        pltlib.add_cbar(axa[1,1], im, arr=diff_euler_align, clim=dz_clim, label=None)
        axa[1,1].set_title('Elev. Diff. After (m)')

        #Tried to insert Nuth fig here
        #ax_nuth.change_geometry(1,2,1)
        #f.axes.append(ax_nuth)

        bins = np.linspace(dz_clim[0], dz_clim[1], 128)
        axa[1,2].hist(diff_euler_orig_compressed, bins, color='g', label='Before', alpha=0.5)
        axa[1,2].hist(diff_euler_align_compressed, bins, color='b', label='After', alpha=0.5)
        axa[1,2].axvline(0, color='k', linewidth=0.5, linestyle=':')
        axa[1,2].set_xlabel('Elev. Diff. (m)')
        axa[1,2].set_ylabel('Count (px)')
        axa[1,2].set_title("Source - Reference")
        #axa[1,2].legend(loc='upper right')
        #before_str = 'Before\nmean: %0.2f\nstd: %0.2f\nmed: %0.2f\nnmad: %0.2f' % tuple(diff_euler_orig_stats[np.array((3,4,5,6))])
        #after_str = 'After\nmean: %0.2f\nstd: %0.2f\nmed: %0.2f\nnmad: %0.2f' % tuple(diff_euler_align_stats[np.array((3,4,5,6))])
        before_str = 'Before\nmed: %0.2f\nnmad: %0.2f' % tuple(diff_euler_orig_stats[np.array((5,6))])
        axa[1,2].text(0.05, 0.95, before_str, va='top', color='g', transform=axa[1,2].transAxes)
        after_str = 'After\nmed: %0.2f\nnmad: %0.2f' % tuple(diff_euler_align_stats[np.array((5,6))])
        axa[1,2].text(0.65, 0.95, after_str, va='top', color='b', transform=axa[1,2].transAxes)

        suptitle = '%s\nx: %+0.2fm, y: %+0.2fm, z: %+0.2fm' % (os.path.split(outprefix)[-1], dx_total, dy_total, dz_total)
        f.suptitle(suptitle)
        f.tight_layout()
        plt.subplots_adjust(top=0.90)

        fig_fn = outprefix + '%s_align.png' % xyz_shift_str_cum
        print("Writing out figure: %s" % fig_fn)
        f.savefig(fig_fn, dpi=300)

    #Removing residual planar tilt can introduce additional slope/aspect dependent offset
    #Want to run another round of main dem_align after removing planar tilt
    if tiltcorr:
        print("\n Rerunning after applying tilt correction \n")
        #Create copy of original arguments
        import copy
        args2 = copy.copy(args)
        #Use aligned, tilt-corrected DEM as input src_fn for second round
        args2.src_fn = align_fn 
        #Assume we've already corrected most of the tilt during first round (also prevents endless loop)
        args2.tiltcorr = False
        main2(args2)

def main(argv=None):
    parser = getparser()
    args = parser.parse_args()
    main2(args)

if __name__ == "__main__":
    main()
