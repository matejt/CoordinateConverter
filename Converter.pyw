__author__ = 'Matej'

import pyproj
import tkMessageBox
import ttk
from Tkinter import *
from settings import coord_system_EPSG_RigData


class EPSG(object):
    # coordinate systems and corresponding EPSG codes
    def __init__(self, parent, group_name, column=0, row=0):

        self.CS_input = StringVar()
        self.CS_output = StringVar()

        coord_system_EPSG_keys = coord_system_EPSG_RigData.keys()
        coord_system_EPSG_keys.sort()

        labelframe = ttk.Labelframe(parent, text=group_name, padding="10 10 10 10")
        labelframe.grid(column=column, row=row)

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
    def __init__(self, parent, group_name, column=0, row=0):

        self.northing_string = StringVar()
        self.easting_string = StringVar()

        labelframe = ttk.Labelframe(parent, text=group_name, padding="10 10 10 10")
        labelframe.grid(column=column, row=row)
        labelframe.pack(side=LEFT, fill=X)

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



class Converter(object):
    def __init__(self):

        root = Tk()
        root.title("Coordinate converter")
        root.resizable(FALSE,FALSE)
        # Frame to contain other widgets
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0)

        # adding widgets
        self.epsg = EPSG(mainframe,'Coordinate Systems',column=0, row=0)
        self.input_coordinates = Coordinates(mainframe,'Input coordinates', column=0, row=1)
        self.output_coordinates = Coordinates(mainframe,'Output coordinates', column=0, row=2)

        ttk.Button(mainframe, text='Clear Results', command=self.clear).grid(column=0, row=3, sticky=(W, E))
        ttk.Button(mainframe, text='Transform', command=self.transform).grid(column=0, row=4, sticky=(W, E))

        # Northing_in.focus()

        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
        root.bind('<Return>', self.transform)
        root.mainloop()

    def transform(self,*args):
        epsg_input = coord_system_EPSG_RigData.get(self.epsg.CS_input.get(),None)
        epsg_output = coord_system_EPSG_RigData.get(self.epsg.CS_output.get(),None)

        coordinate_system_in = pyproj.Proj("+init=EPSG:%i" % epsg_input)
        coordinate_system_out = pyproj.Proj("+init=EPSG:%i" % epsg_output)

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
