__author__ = 'Matej'

import pyproj
import tkMessageBox
import ttk
import os
import pyperclip
from Tkinter import *
from settings import coord_system_EPSG_RigData


class EPSG(object):
    # coordinate systems and corresponding EPSG codes
    def __init__(self, parent, group_name, column=0, row=0, columnspan=1, rowspan=1):

        self.CS_input = StringVar()
        self.CS_output = StringVar()

        coord_system_EPSG_keys = coord_system_EPSG_RigData.keys()
        coord_system_EPSG_keys.sort()

        labelframe = ttk.Labelframe(parent, text=group_name, padding="10 10 10 10")
        labelframe.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan)

        ttk.Label(labelframe, text='Input Coordinate System:').grid(column=0, row=0, sticky=E)
        ttk.Label(labelframe, text='Output Coordinate System:').grid(column=0, row=1, sticky=E)

        EPSG_in = ttk.Combobox(labelframe, width = 50, textvariable=self.CS_input, state='readonly')
        EPSG_in.grid(column=1, row=0, sticky=(W, E))
        EPSG_in['values'] = coord_system_EPSG_keys

        EPSG_out = ttk.Combobox(labelframe, width = 50, textvariable=self.CS_output, state='readonly')
        EPSG_out.grid(column=1, row=1, sticky=(W, E))
        EPSG_out['values'] = coord_system_EPSG_keys

        for combo in [EPSG_in,EPSG_out]:
            combo.current(0)


class Coordinates(object):
    def __init__(self, parent, group_name, column=0, row=0, columnspan=1, rowspan=1):

        self.northing_string = StringVar()
        self.easting_string = StringVar()

        labelframe = ttk.Labelframe(parent, text=group_name, padding="10 10 10 10")
        # labelframe.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=W)
        labelframe.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan)

        ttk.Label(labelframe, text='Northing:').grid(column=0, row=0, sticky=E)
        ttk.Label(labelframe, text='Easting:').grid(column=0, row=1, sticky=E)

        vcmd = (parent.register(self.onValidate), '%P')

        northing = ttk.Entry(labelframe, width=15, textvariable=self.northing_string, validate="key", validatecommand=vcmd)
        northing.grid(column=1, row=0, sticky=(W, E))

        easting = ttk.Entry(labelframe, width=15, textvariable=self.easting_string, validate="key", validatecommand=vcmd)
        easting.grid(column=1, row=1, sticky=(W, E))

    def onValidate(self, P):
        # print 'P=%s' % P
        try:
            float(P)
            return True
        except:
            return False

    def copy_to_clipboard(self):
        E, N = float(self.northing_string.get()), float(self.easting_string.get())
        if abs(E) < 360 and abs(N) < 360:
            pyperclip.copy('%.6f, %.6f' % (E, N))
        else:
            pyperclip.copy('%.2f, %.2f' % (E, N))

class Converter(object):
    def __init__(self):

        root = Tk()
        root.title("Coordinate converter")
        root.resizable(FALSE,FALSE)

        # Frame that contains other widgets
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0)

        # adding widgets
        self.epsg = EPSG(mainframe,'Coordinate Systems',column=0, row=0, columnspan=1)
        self.input_coordinates = Coordinates(mainframe,'Input coordinates', column=0, row=1)
        self.output_coordinates = Coordinates(mainframe,'Output coordinates', column=0, row=2)

        # adds image
        path = os.path.dirname(__file__)
        im = PhotoImage(file=os.path.join(path,'img/normal_Earth-Rise,-Apollo-8,-December-1968.gif'))
        # ttk.Label(mainframe, image=im).grid(column=1, row=1, rowspan=2,sticky=W+E+N+S)
        # ttk.Label(mainframe, image=im).place(x=0, y=0, relwidth=1, relheight=1)

        ttk.Button(mainframe, text='Copy to Clipboard', command=self.output_coordinates.copy_to_clipboard).grid(column=0, row=3, sticky=(W, E))
        ttk.Button(mainframe, text='Clear Results', command=self.clear).grid(column=0, row=4, sticky=(W, E))
        ttk.Button(mainframe, text='Transform', command=self.transform).grid(column=0, row=5, sticky=(W, E))

        # Northing_in.focus()
        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
        root.bind('<Return>', self.transform)
        root.mainloop()

    def transform(self,*args):
        epsg_input = coord_system_EPSG_RigData.get(self.epsg.CS_input.get(),None)
        epsg_output = coord_system_EPSG_RigData.get(self.epsg.CS_output.get(),None)

        # if '' in [epsg_input, epsg_output]:
        #     tkMessageBox.showerror(title='Empty input', message='Enter input coordinates')

        coordinate_system_in = pyproj.Proj(init='epsg:%i' % epsg_input, preserve_units=True)
        coordinate_system_out = pyproj.Proj(init='epsg:%i' % epsg_output, preserve_units=True)

        try:
            easting_in = self.input_coordinates.easting_string.get()
            northing_in = self.input_coordinates.northing_string.get()
            east_out, north_out = pyproj.transform(coordinate_system_in, coordinate_system_out, easting_in, northing_in)
            self.output_coordinates.easting_string.set(east_out)
            self.output_coordinates.northing_string.set(north_out)
            # print epsg_input, epsg_output
            # print east_out, north_out
        except (RuntimeError,TypeError,ValueError):
            self.clear()
            tkMessageBox.showerror(title='Unable to transform', message=sys.exc_info())


    def clear(self):
        for x in [self.output_coordinates.northing_string, self.output_coordinates.easting_string]:
            x.set('')
if __name__ == '__main__':
    app = Converter()


    # testing
    # root = Tk()
    # app1 = EPSG(root,'test')
    # app2 = Coordinates(root,'test',0,1)
    # root.mainloop()
