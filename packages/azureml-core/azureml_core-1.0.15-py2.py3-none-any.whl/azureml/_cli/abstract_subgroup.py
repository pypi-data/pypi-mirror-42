# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import pkgutil
import importlib
import inspect
import sys

from abc import ABCMeta, abstractmethod


# Defines an abstract class for a CLI command.
class AbstractSubGroup(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_subgroup_name(self):
        """
        Returns the name of the subgroup.
        This name will be used in the cli command.
        """
        pass

    @abstractmethod
    def get_subgroup_title(self):
        """
        Returns the subgroup title as string. Title is just for informative purposes, not related
        to the command syntax or options. This is used in the help option for the subgroup.
        """
        pass

    @abstractmethod
    def get_nested_subgroups(self):
        """Returns sub-groups of this sub-group."""
        pass

    @abstractmethod
    def get_commands(self):
        """Returns commands associated at this sub-group level.
        """
        pass

    def register_with_azure_cli(self):
        """
        Returns True if the subgroup needs to be registered with azure cli.
        Child classes can override this function to not register their subgroup with azure cli.
        :return:
        :rtype bool:
        """
        return True

    @classmethod
    def compute_nested_subgroups(cls, package_name):
        """A function to compute the list of nested subgroups at this subgroup level.
        This function only  creates objects for the immediate subgroups to this subgroup,
        it doesn't perform any further recursion. This function looks for the
        nested subgroups in all the directories where the file corresponding to this subgroup is
        located. In a nested subgroup package, this function iterates through all modules and adds those modules
        that have a class that is derived from AbstractSubGroup. If this function finds that a module
        has more than one implementation of AbstractSubGroup class, then this function throws
        an error. This function returns a list of object of classes derived from AbstractSubGroup"""

        nested_subgroup_class_objects = []
        subpackage_list = cls.get_all_subpackages(package_name)

        for subpackage_name in subpackage_list:
            subpackage = package_name+"."+subpackage_name
            module_list = cls.get_all_modules(subpackage)

            assert len(module_list) == 1, "subpackage={0} doesn't contain exactly 1 module, which is not supported " \
                                          "according to aml_cli command structure.".format(subpackage)

            module_object = importlib.import_module(subpackage + "." + module_list[0])
            name_class_tuples = inspect.getmembers(module_object, inspect.isclass)
            classes = dict(name_class_tuples)

            assert len(name_class_tuples) == 1, "module={0} doesn't contain exactly 1 class, which is not " \
                                                "supported according to aml_cli command " \
                                                "structure.".format(subpackage + "." + module_list[0])

            for classname in classes:
                # Check that the class is derived from AbstractSubGroup
                assert issubclass(classes[classname], AbstractSubGroup), "class={0} is not a subclass of {1}".format(
                    subpackage + "." + module_list[0] + "." + classname, AbstractSubGroup)

                assert cls._check_for_empty_constructor(classes[classname]), \
                    "class={0} doesn't have empty constructor, which is not supported according to aml_cli command " \
                    "structure.".format(subpackage + "." + module_list[0] + "." + classname)

                class_object = classes[classname]()
                nested_subgroup_class_objects.append(class_object)

        return nested_subgroup_class_objects

    @classmethod
    def get_all_subpackages(cls, package_name):
        """ Returns all subpackages in a package, excluding the modules.
        The package name should be resolvable from the sys.path.
        The names of returned subpackages are relative to this package.
        Like, package_name=A, contains subpackages B, C, D.
        Then, this function returns [B, C, D]. If there are no sub-packages,
        then an empty list is returned."""
        subpackages_list = []
        package_handle = importlib.import_module(package_name)
        for importer, modname, ispkg in pkgutil.iter_modules(package_handle.__path__):
            if ispkg:
                subpackages_list.append(modname)

        return subpackages_list

    @classmethod
    def get_all_modules(cls, package_name):
        """ Returns all modules in a package, excluding the subpackages.
        The package name should be resolvable from the sys.path.
        The names of returned modules are relative to this package.
        Like, package_name=A, contains modules B, C, D.
        Then, this function returns [B, C, D]. If there are no modules,
        then an empty list is returned."""
        modules_list = []
        package_handle = importlib.import_module(package_name)
        for importer, modname, ispkg in pkgutil.iter_modules(package_handle.__path__):
            if not ispkg:
                modules_list.append(modname)
        return modules_list

    @classmethod
    def _check_for_empty_constructor(cls, class_handle):
        """ The function takes the class handle and checks if the class' constructor is empty or not."""
        # TODO: No easy way to inspect a constructor in python 2.7.
        # So, we are skipping it. This is just an inspection while adding new command modules,
        # so there is no problem in skipping this, anyways it gets tested in python 3.
        if sys.version_info[0] < 3:
            return True

        arguments_tuple = inspect.getfullargspec(class_handle.__init__)
        if arguments_tuple.args == ['self'] and arguments_tuple.kwonlyargs == []:
            return True
        else:
            return False
