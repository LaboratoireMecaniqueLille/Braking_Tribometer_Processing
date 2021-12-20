# coding: utf-8

import matplotlib.pyplot as plt
import math
import matplotlib

# give values of correcting offsets, to reposition data on image
Xp_offset = 0
Yp_offset = 0
Zp_offset = 0.

# give values of tilt correction around each axis in microns
tilt_corr_height_y = 0
tilt_corr_height_x = 0


# Read data from file

separator = ','
directory = r'C:\Users\mbriatte\Desktop\02 - Modelisation_et_' \
            r'caracterisations\Profilometre\Fichier_python_Profilo_Edouard/'
fichier = '20180704_prDAT_07.asc'

fichier = open(directory + fichier, "r")

with fichier as source:
    lines = fichier.readlines()

    # Search in file header for parameters to read data

hl = 0
wl = 0
lc = 0
sz = 0
mg = 0

for L in range(200):

    # "RAW DATA" is the string announcing the last line of header and the
    # start of profile data
    if not (lines[L].split(separator)[0].find("RAW_DATA") == -1) and hl == 0:
        head_length = L+1
        hl = 1

    # raw height data has to be multiplied by wavelength of the measuring
    # light to obtain actual height
    if not (lines[L].split(separator)[0].find("Wavelength") == -1) and wl == 0:
        wavelength = float(lines[L].split(separator)[3])
        wl = 1

    # Corresponds to the size of one pixel on the given image. not the actual
    # size of a pixel on the sensor.
    # if not (lines[L].split(separator)[0].find("Pixel_size") == -1) \
    #     and lc == 0:
        # Pixel_size_X = float(lines[L].split(separator)[3])  # * 1000
        # Pixels are 7/6 times bigger in y direction than in x
        # Pixel_size_Y = Pixel_size_X * 7/6
        # lc = 1

    # read the size of the image in pixels, on X and Y
    if not (lines[L].split(separator)[0].find("X Size") == -1) and sz == 0:
        Wyko_Nx = float(lines[L].split(separator)[1])
        Wyko_Ny = float(lines[L+1].split(separator)[1])
        sz = 1
        
    if not (lines[L].split(separator)[0].find("Magnification") == -1) and \
            mg == 0:
        mag = float(lines[L].split(separator)[3])
        mg = 1

# sometimes, strangely, files are recorded with a shorter header, missing
# information. they will be entered here
if head_length < 12:
    wavelength = float(input('Please enter Wavelength: '))
    mag = float(input('Please enter Magnification: '))

# for a magnification of 5.22, pixel size is 0.001609 meters. we derive values
# at other magnifications from this
Pixel_size_X = 0.001609 * 5.22 / mag * 1000
# Pixels are 7/6 times bigger in y direction than in x
Pixel_size_Y = Pixel_size_X * 7 / 6
    
print("Pixel_size_X", Pixel_size_X)
# Load the lines containing data in "lines"
lines = lines[head_length:head_length + int(Wyko_Nx * Wyko_Ny)]

# find the last of the lines
last_line = lines[int(Wyko_Nx * Wyko_Ny)-1].split(separator)

# if the value of the last line equals image size in pixel , then the
# coordinates of the data points are given in pixels. else they're given
# in distance
if float(last_line[0]) == float(Wyko_Nx - 1):
    d = 0
    unit_converter = 1.
    
elif float(last_line[0]) > 400000:
    d = 1
    unit_converter = 1/1000
else:
    d = 2

    # if the Y coordinate of the last line is big, then the unit must be
    # micrometers. Else it is millimeters. educated guess that worked sor far.
    # apparently nothing better to get this ...
    if float(last_line[1]) > 25:
        unit_converter = 1.
    else:
        unit_converter = 1000.

print("d =", d)

# Compute the image size in microns, from size in pixels and pixel size
Wyko_Sx_2 = Wyko_Nx * Pixel_size_X
Wyko_Sy_2 = Wyko_Ny * Pixel_size_Y

# Show some data about the image to the user
print('fileheader length :', head_length)
print('wavelength :', wavelength)
print('Pixel_size_X :', Pixel_size_X)
print('Pixel_size_Y :', Pixel_size_Y)
print('Wyko_Nx :', Wyko_Nx, 'Wyko_Ny :', Wyko_Ny)
print('Wyko_Sx_2 :', Wyko_Sx_2, 'Wyko_Sy_2 :', Wyko_Sy_2)
print('Magnification :', mag)

# create empty lists for profile data
# Xp, Yp, Zp = [], [], []
Xp, Yp, Zp, Xbad, Ybad = [], [], [], [], []
# fill these lists with profile data

length = int(len(lines)/1)

for i in range(length):
    line = lines[i].split(separator)
    if d == 0:
        Xp.append(float(line[0]) * unit_converter * Pixel_size_X)
        Yp.append(float(line[1]) * unit_converter * Pixel_size_Y)
        
    elif d == 1:
        Xp.append(float(int(float(line[0]) * unit_converter) * Pixel_size_X))
        Yp.append(float(int(float(line[1]) * unit_converter) * Pixel_size_Y))
        
    elif d == 2:
        Xp.append(float(line[0]) * unit_converter)
        Yp.append(float(line[1]) * unit_converter)
    Zp.append(line[2])
    
    # Replace "bad" values by "nan" and remove values that are too low and/or
    # too high (for contrast' sake)
    if Zp[i] == 'Bad\n':  # or float(Zp[i]) * wavelength / 1000. + Zp_offset < -10 or float(Zp[i]) * wavelength / 1000. + Zp_offset > 8:
        Zp[i] = float('nan')
        # Xbad.append(Xp[i])
        # Ybad.append(Yp[i])

    elif float(Zp[i])*wavelength/1000. + Zp_offset < -9 or \
            float(Zp[i]) * wavelength / 1000. + Zp_offset > 8:
        Xbad.append(Xp[i])
        Ybad.append(Yp[i])
        Zp[i] = float('nan')

    # convert raw Zp data to actual height in microns and add eventual
    # correcting offset
    else:
        Zp[i] = float(Zp[i])*wavelength/1000. + Zp_offset

print(len(Xbad), len(Ybad))
       
del lines  # get rid of this hefty bunch of raw data


# Conditionning and correcting data


# Tilt correction along X and Y (Z_corr measured visually on plot)
tilt_corr_ang_y = math.atan(float(tilt_corr_height_y) / float(Wyko_Sx_2))
tilt_corr_ang_x = math.atan(float(tilt_corr_height_x) / float(Wyko_Sy_2))
# Do not use that. SOUNDS GOOD, DOESN'T WORK


# Plotting


font_sz_med = 30  # define standard sizes for text on the graphs
font_sz_big = 35


# define plots parameters with functions
def PlotStyle_Common_feats():
    matplotlib.use("Qt5Agg")
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()
    # plt.tick_params(labelsize = font_sz_big)
    # plt.grid(b=True, which='major', color='k', linestyle='-')
    # plt.minorticks_on()
    # plt.grid(b=True, which='minor', color='0.5', linestyle='-')
    # plt.xlim([0, 1000])
    # plt.ylim([0, 12000])


def PlotStyle_Annotations():
    plt.annotate('tilt corr ang_x : %s deg    '
                 'tilt corr ang_y : %s deg  ' %
                 (round(math.degrees(tilt_corr_ang_x), 3),
                  round(math.degrees(tilt_corr_ang_y), 2)), (0, 0), (0, -48))
    plt.annotate(r'Wyko prof. data offset ($\mu$m) :      '
                 '/X : %s    '
                 '/Y : %s    '
                 '/Z : %s' % (Xp_offset, Yp_offset, Zp_offset),
                 (0, 0), (0, -51))
    plt.annotate('Wyko prof. source data file : %s    ' %
                 source_file_prof, (0, 0), (0, -54))
    

# plot profile map


print(max(Zp), min(Zp))


colormap = 'CMRmap'

print("plotting")
fig0 = plt.scatter(Xp, Yp, s=2, c=Zp, marker='s', lw=0, cmap=colormap)
# alternative :  cmap='plasma'   cmap='magma'

cb = plt.colorbar()
cb.set_label(r'Profondeur ($\mu$m)', labelpad=10, y=0.5)
# color_bar_labels = []

# for label in cb.ax.get_yticklabels():
#     color_bar_labels.append(label.get_text())
    
# cb.ax.set_yticklabels(color_bar_labels)

plt.scatter(Xbad, Ybad, s=2, c="0.5", marker='s', lw=0)

plt.suptitle('Mesure Profilomètre', fontsize=font_sz_big)
plt.xlabel(r'X ($\mu$m)')
plt.ylabel(r'Y ($\mu$m)')

# plt.legend(loc='lower left')
# plt.axis('equal')
PlotStyle_Common_feats()


plt.margins(0, 0)
plt.show()
plt.savefig(directory + f'Test.png')

print("End")
# plt.show()
