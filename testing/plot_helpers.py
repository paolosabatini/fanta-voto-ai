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
    return box_vs_var_plot (data, labels, xlabel, ylabel, xlim, ylim, decos )

def box_vs_var_plot (data, labels, xlabel=None, ylabel=None, xlim=None, ylim=None, decos = []):
    
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



def poly_fitter (x, y, degree = 1, cov = False):
    pars, Cpars = np.polyfit (x, y, deg=degree, cov=True)
    xx= np.vstack([x**(degree-i) for i in range(degree+1)]).T
    y_lin = np.dot (xx,pars)
    if cov:
        C_y_lin = np.dot(xx, np.dot(Cpars, xx.T)) # C_y_lin = xx*Cpars*xx.T
        sig_y_lin = np.sqrt(np.diag(C_y_lin))  # Standard deviations are sqrt of diagonal
        return y_lin, sig_y_lin
    return y_lin
            
def scat_plot_diff_classes (list_of_data, labels, xlabel, ylabel,  xaxislabel=None, yaxislabel=None, xlim=None, ylim=None, decos = [], do_fit=False, do_legend = True):

    markers = [4, 5, 6, 7]
               
    fig,ax = plt.subplots()

    for ids, ds in enumerate (list_of_data):
        ax.scatter (ds[xlabel].to_numpy(), ds[ylabel].to_numpy(), label = labels[ids], marker = markers[ids])

    if do_fit:
        degree = 1
        prediction = poly_fitter ( ds[xlabel].to_numpy(), ds[ylabel].to_numpy(), degree )
        ax.plot(ds[xlabel].to_numpy(), prediction, linestyle='dotted')

        
    if xlabel: ax.set_xlabel(xaxislabel, fontsize=10)
    if ylabel: ax.set_ylabel(yaxislabel, fontsize=10)
    if xlim: plt.xlim (xlim[0], xlim[-1])
    if ylim: plt.ylim (ylim[0], ylim[-1])

    draw_vector_labels (0.05,0.95, ax, decos)
    if do_legend: ax.legend()
    
    insert_logo (ax)

    
    return fig


def get_bins_on_this_column (col, nbins = 20, integer = False):
    xmin = col.min()
    xmax = col.max()
    if integer:
        nbins = xmax-xmin+1
    return np.linspace(xmin, xmax, nbins)

def hist_per_classes (df, classification = None, variable = '', nbins = 20, integer = False, xaxislabel=None, yaxislabel=None, xlim=None, ylim=None, decos = []):
    from analysis_helpers import encode_position

    fig, ax = plt.subplots()
    if variable: values = df [variable]
    if classification == 'position':
        from mycolorpy import colorlist as mcp
        colors = mcp.gen_color(cmap="Set2", n=8)
        mybins = get_bins_on_this_column (df[variable], nbins, integer = integer)
        plt.hist ( df [variable] [df ['Ruolo'] == encode_position ('G')].to_numpy(), mybins, facecolor = colors[0], edgecolor = colors[0], alpha = 0.5, density = True, label = 'Goalkeeper')
        plt.hist ( df [variable] [df ['Ruolo'] == encode_position ('D')].to_numpy(), mybins, facecolor = "none", edgecolor = colors[1], linestyle = "dashed", linewidth=2, density = True, histtype = "step" , label = 'Defender')
        plt.hist ( df [variable] [df ['Ruolo'] == encode_position ('M')].to_numpy(), mybins, facecolor = "none", edgecolor = colors[2], linestyle = "dashed", linewidth=2, density = True, histtype = "step" , label = 'Midfielder')
        plt.hist ( df [variable] [df ['Ruolo'] == encode_position ('F')].to_numpy(), mybins, facecolor = colors[-2], edgecolor = colors[-2], alpha = 0.5, density = True , label = 'Forward')
        
        ax.legend()
    elif classification == 'pred_vs_meas':
        from mycolorpy import colorlist as mcp
        colors = mcp.gen_color(cmap="Set2", n=8)
        mybins = np.linspace (-0.25,10.75, num=23)
        plt.hist ( df ['target'].to_numpy(), mybins, color = colors[0], alpha = 0.5, density = False, label = 'Measured')
        # df ['prediction'].plot (kind='bar',  mybins, color = None, yerr= , alpha = 1.0, density = True, label = 'Predicted')
        import pandas as pd
        df ['prediction_bin'] = pd.cut (df ['prediction'], mybins, labels = mybins[:-1]+0.25) 
        pred_hist_entries = df.groupby ( by = 'prediction_bin').size()
        pred_hist_err = pred_hist_entries**0.5
        print 
        plt.errorbar ( x = pred_hist_entries.index, y = pred_hist_entries.values, yerr = pred_hist_err.values, label = 'Predicted',
                       fmt = 'o')
        
        ax.legend()
        
    elif not classification:
        from mycolorpy import colorlist as mcp
        colors = mcp.gen_color(cmap="Set2", n=8)
        mybins = get_bins_on_this_column (df[variable], nbins, integer = integer)
        plt.hist ( df [variable].to_numpy(), mybins, color = colors[0], alpha = 0.5, density = True)

    if xaxislabel: ax.set_xlabel(xaxislabel, fontsize=10)
    if yaxislabel: ax.set_ylabel(yaxislabel, fontsize=10)
    if xlim: plt.xlim (xlim[0], xlim[-1])
    if ylim: plt.ylim (ylim[0], ylim[-1])

    insert_logo (ax)
    draw_vector_labels (0.05,0.95, ax, decos)
    return fig



def compare_prediction_and_target ( x, y1, y2, xaxislabel = None, yaxislabel = None, y1label = None, y2label = None, xlim = None, ylim = None, decos = [] ):

    fig, ax = plt.subplots()
    line1, = ax.plot (x,y1)
    if y1label: line1.set_label (y1label)
    line2, = ax.plot (x,y2)
    if y2label: line2.set_label (y2label)
 
    if xaxislabel: ax.set_xlabel(xaxislabel, fontsize=10)
    if yaxislabel: ax.set_ylabel(yaxislabel, fontsize=10)
    if xlim: plt.xlim (xlim[0], xlim[-1])
    if ylim: plt.ylim (ylim[0], ylim[-1])

    
    
    insert_logo (ax)
    draw_vector_labels (0.05,0.95, ax, decos)

    if (y1label or y2label): ax.legend()
    
    return fig
