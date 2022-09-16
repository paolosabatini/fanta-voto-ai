#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

# def set_style ():

#     sns.color_palette("pastel")
#     sns.set_theme()

def insert_logo (ax):
    xmin, xmax = ax.get_xlim()
    xran = (xmax-xmin)
    ymin, ymax = ax.get_ylim()
    yran = (ymax-ymin)
    ax.text (xmax, ymax+0.025*(yran), r'$FantaWoman$ VotoAI', va='center', ha='right', fontsize=8 )
    
    

def scale_rotation (angle, units = 'deg'):
    scale_factor = 36./45.
    if units != 'deg': return scale_factor*angle*360/(2*math.pi)
    return scale_factor*angle


def correlation_plot ( xarray, yarray, xlabel=None, ylabel=None, xlim=None, ylim=None, labels = []) :
    
    x = xarray.flatten ()
    y = yarray.flatten ()
  
    fig,ax = plt.subplots()
       
    if xlabel: ax.set_xlabel(xlabel, fontsize=10)
    if ylabel: ax.set_ylabel(ylabel, fontsize=10)
    if xlim: plt.xlim (xlim[0], xlim[-1])
    if ylim: plt.ylim (ylim[0], ylim[-1])

    ## linear fit + plotting uncertainty
    x_fit = x if not xlim else np.append(x,xlim)
    x_fit = np.sort (x_fit)
    degree = 1
    pars, Cpars = np.polyfit (x, y, deg=degree, cov=True)
    xx= np.vstack([x_fit**(degree-i) for i in range(degree+1)]).T
    y_lin = np.dot (xx,pars)
    ax.plot(x_fit, x_fit, ':C7') 
    ax.scatter ( x= x, y = y )
    ax.plot(x_fit, y_lin, ':C0')
    C_y_lin = np.dot(xx, np.dot(Cpars, xx.T)) # C_y_lin = xx*Cpars*xx.T
    sig_y_lin = np.sqrt(np.diag(C_y_lin))  # Standard deviations are sqrt of diagonal
    ax.fill_between(x_fit, y_lin+sig_y_lin, y_lin-sig_y_lin, alpha=.25, color = "C0")


    
    # now filling with text
    xmin, xmax = ax.get_xlim()
    xran = (xmax-xmin)
    ymin, ymax = ax.get_ylim()
    yran = (ymax-ymin)
    ax.text( xmin + 0.7*xran, ymin + 0.75*yran, 'Perfect prediction', va='center', ha='center', rotation = scale_rotation(45), color='C7')
    ax.text( xmin + 0.9*xran, pars[0]*(xmin + 0.8*xran)+pars[1], 'Linear model', rotation = scale_rotation(math.atan(pars[0]), 'rad'), va='center', ha='center', color='C0')
    # ax.text( , 'Perfect prediction', rotation = 37, color='C7')

    legend_y = 0.9
    legend_x = 0.05
    legend_step = 0.05
    ax.text (xmin + legend_x*xran, ymin + legend_y*yran, r'Linear model: $y = ax + b$', va='center', ha='left')
    ax.text (xmin + (legend_x)*xran, ymin + (legend_y-legend_step)*yran, r'   $a = %.2f\pm%.2f$' % (pars[0], (Cpars[0][0])**0.5), va='center', ha='left')
    ax.text (xmin + (legend_x)*xran, ymin + (legend_y-2*legend_step)*yran, r'   $b = %.2f\pm%.2f$' % (pars[1], (Cpars[1][1])**0.5), va='center', ha='left')


    insert_logo (ax)
        
    return fig



def residual_vs_var_plot (data, labels, xlabel=None, ylabel=None, xlim=None, ylim=None, decos = []):
    
    fig,ax = plt.subplots()

    means = [ x.mean() for x in data ]
    medians = [ np.median(x) for x in data ]
    stds = [ x.std() for x in data ]

    
    
    ax.yaxis.grid(True)
    if xlabel: ax.set_xlabel(xlabel, fontsize=10)
    if ylabel: ax.set_ylabel(ylabel, fontsize=10)
    if xlim: plt.xlim (xlim[0], xlim[-1])
    if ylim: plt.ylim (ylim[0], ylim[-1])

    ax.boxplot ( data, labels = labels,
                 showmeans=True)
    #        ax.scatter ( x= x, y = y )

    ymin, ymax = ax.get_ylim()
    mean_yf = 0.78
    mean_y = ymin + mean_yf*(ymax-ymin)
    std_yf = 0.74
    std_y = ymin + std_yf*(ymax-ymin)
    med_yf = 0.7
    med_y = ymin + med_yf*(ymax-ymin)

    statsize=8
    for itick,xtick in enumerate(ax.get_xticks()):
        ax.text (xtick, med_y, r'$M = %.2f$' % medians [itick], va='center', ha='center', size=statsize)
        ax.text (xtick, mean_y, r'$\mu = %.2f$' % means [itick], va='center', ha='center', size=statsize)
        ax.text (xtick, std_y, r'$\sigma = %.2f$' % stds [itick], va='center', ha='center', size=statsize)


    draw_vector_labels (0.05,0.95, ax, decos)
    draw_vector_labels (0.8, 0.95, ax, [r'$M$ := median', r'$\mu$ := mean', r'$\sigma$ := std. dev.'], size=8, step=0.03)
    
    insert_logo (ax)
    return fig


def draw_vector_labels ( xf, yf, ax, labels, size = None, step = 0.05):
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    xran = xmax-xmin
    yran = ymax-ymin
    for ilabel,label in enumerate (labels):
        if size:
            ax.text ( xmin + xf*xran, ymin + (yf-ilabel*step)*yran, label, va='center', ha='left', fontsize=size)
        else:
            ax.text ( xmin + xf*xran, ymin + (yf-ilabel*step)*yran, label, va='center', ha='left')



def scat_plot_diff_classes (list_of_data, labels, xlabel, ylabel,  xaxislabel=None, yaxislabel=None, xlim=None, ylim=None, decos = []):

    fig,ax = plt.subplots()

    for ids, ds in enumerate (list_of_data):
        ax.scatter (ds[xlabel].to_numpy(), ds[ylabel].to_numpy(), label = labels[ids])
        
        
    if xlabel: ax.set_xlabel(xaxislabel, fontsize=10)
    if ylabel: ax.set_ylabel(yaxislabel, fontsize=10)
    if xlim: plt.xlim (xlim[0], xlim[-1])
    if ylim: plt.ylim (ylim[0], ylim[-1])

    
    return fig
