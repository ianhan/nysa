# -*- coding: utf-8 -*-
import sys
import os
import json
import glob

from PyQt4.QtCore import QObject
from PyQt4.QtCore import SIGNAL

from ninja_ide.core import file_manager


sys.path.append(os.path.join( os.path.dirname(__file__),
                                os.pardir,
                                os.pardir,
                                "editor",
                                "fpga_designer"))

from controller.wishbone_controller import WishboneController
from controller.axi_controller import AxiController
from fpga_designer import FPGADesigner

sys.path.append(os.path.join( os.path.dirname(__file__),
                                os.pardir,
                                os.pardir,
                                "editor",
                                "constraint_editor"))

from constraint_editor import ConstraintEditor


'''
Functions independent of the project used to build/simulate/debug
'''

DESIGNER_EXT = "ibd"



class IBuilder (QObject):
    output = None

    def __init__(self, output, locator):
        self.output = output
        self.locator = locator
        self.editor = self.locator.get_service('editor')
        self.explorer = self.locator.get_service('explorer')
        self.builder = self.locator.get_service('misc')._misc

        self.output.Debug(self, "create ibuilder!")
        self.designers = {}
        self.load_designers()
        self.controller = None
        self.actions = None
        self.commands = {}
        self.setup_commands()

    def setup_controller(self, filename):
        d = {}
        controller = None
        #try:
        f = open(filename, "r")
        d = json.loads(f.read())
        #except IOError, err:
        #    raise FPGADesignerError("IOError: %s" % str(err))

        #except TypeError, err:
        #    raise FPGADesignerError("JSON Type Error: %s" % str(err))

        #A Pathetic factory pattern, select the controller based on the bus
        print "Getting Wishbone Controller"
        if d["TEMPLATE"] == "wishbone_template.json":
            controller = WishboneController(output = self.output, config_dict = d)
        elif d["TEMPLATE"] == "axi_template.json":
            controller = AxiController(self, self.output)
        else:
            raise FPGADesignerError(    "Bus type (%s) not recognized, view " +
                                        "controller cannot be setup, set the " +
                                        "TEMPLATE value to either " +
                                        "wishbone_template or " +
                                        "axi_tmeplate.json" % str(d["TEMPLATE"])
                                   )
        return controller

    def setup_commands(self):
        #This is sort of like the actions for the entire IDE but I only need
        #This locally (for ibuilder)
        self.commands["constraint_editor"] = self.open_constraint_editor


    def open_constraint_editor(self, view_controller, name = None):
        print "open constraint editor"
        tab_manager = self.editor.get_tab_manager()
        ce = view_controller.get_constraint_editor()
        if ce is None or (tab_manager.is_open(ce) == -1):
            self.output.Debug(self, "Constraint editor is not open")
            if ce is not None: 
                self.output.Debug(self, "There is a bogus constraint editor in the controller")
            ce = ConstraintEditor(parent=tab_manager,
                                  actions=self.actions,
                                  output=self.output,
                                  project_name = view_controller.get_project_name())

            name = "%s ce" % view_controller.get_project_name()
            tab_manager.add_tab(ce, name)
            view_controller.initialize_constraint_editor(ce)

        else:
            tab_manager.move_to_open(ce)


    def file_open(self, filename):
        ext = file_manager.get_file_extension(filename)
        if ext == DESIGNER_EXT:
            self.output.Debug(self, "Found designer extension")
            tab_manager = self.editor.get_tab_manager()

            name = filename.split(os.path.sep)[-1]

            fd = None
            index = -1
            #filename = None

            if name in self.designers.keys():
                fd, index, filename = self.designers[name]
                #we have a reference to this in the local
                self.output.Debug(self, "Manager open vaue: %d" % tab_manager.is_open(fd))
                #Check to see if the widget is in the tab manager
                if tab_manager.is_open(fd) == -1:
                    self.output.Debug(self, "Did not find name in opened tabs")
                    if name in self.designers.keys():
                        del self.designers[name]

                else:
                    tab_manager.move_to_open(fd)
                    self.output.Debug(self, "FPGA Designer is already is open")


            if name not in self.designers.keys():
                self.output.Debug(self, "Open up a new tab")
                project = self.explorer._explorer.get_project_given_filename(filename)
                #Not Opened
                fd = FPGADesigner(actions=self.actions,
                                  commands = self.commands,
                                  filename = filename,
                                  project=project,
                                  parent=tab_manager,
                                  output=self.output)

                #I'm assuming there is no controller set already so create a new one
                controller = self.setup_controller(filename)
                fd.set_controller(controller)

                index = tab_manager.add_tab(fd, name)
                self.designers[name] = (fd, index, filename)
                controller.initialize_view()
                fd.initialize_slave_lists()

            return True

        return False

    def file_save(self, editor):
        filename = editor.ID
        ext = file_manager.get_file_extension(filename)
        if ext == DESIGNER_EXT:
            self.output.Debug(self, "Found designer extension")
            return True

        return False

    def file_closed(self, filename):
        self.output.Debug(self, "Filename: %s" % filename)
        name = filename.split(os.path.sep)[-1]

        if filname in self.designers.keys():
            fd = None
            index = -1
            filename = None
            fd, index, filename = self.designers[name]
            self.output.Debug(self, "Remove: %s from designer" % filename)
            tab_manager = self.editor.get_tab_manager()
            #Go to the correct tab
            tab_manager.remove_tab(index)
            name = filename.split(os.path.sep)[-1]
            self.designers.remove(filename)



    def load_designers(self):
        tab_manager = self.editor.get_tab_manager()


