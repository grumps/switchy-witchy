# -*- coding: utf-8 -*-

"""Traps capture varying events within the system"""
import psutil


class Trap(object):
    """
    An alarm or trigger, to be tripped by a process.
    """

    def __init__(self, properties):
        self.process = Proc.create_watch(properties)


class MemoryTrap(object):

    def max_memory(self):
        """
        some precent of system memory
        """
        pass


class CpuTrap(object):

    def max_cpu_usage(self):
        """
        some precent of system cpu
        """
        pass


class Proc(psutil.Process):
    """
    A subclass of :class:`psutil.Process`
    """

    @classmethod
    def _parent_walk(cls, current_proc):
        """
        recursive function to return the top parential proc
        NOTE: currently we are basing only on name of the process
        as such it may present issues with properly id' the parent
        possible solution - look at os module, or possible systemd
        but could get ugly with various systems. e.g. chrome,
        chrome-sandbox
        :param current_proc :class:`psutil.Process`: Process instance Process instance
        :return Proc.id: Process Id
        :rtype int:
        """
        parent = current_proc.parent()
        try:
            if current_proc.name() != parent.name():
                return current_proc.pid
        except AttributeError:
            # We've traveresed all the way to PID 1,
            # `process.parent()` returns None
            return current_proc.pid
        return cls._parent_walk(current_proc.parent())

    @classmethod
    def _is_match(cls, proc, properties):
        """
        True if all configured process properties match a process.
        we are checking if all fields provided
        match, the current proc.
        access each object's attr, via a 'string'
        :param proc: the actual process, `psutil.Process`
        :return bool:
        :rtype bool:
        """
        property_fields_match = [properties.get(field) == getattr(proc, field)()
                                 for field in properties.keys()]
        return all(property_fields_match)

    @classmethod
    def create_watch(cls, properties):
        """
        finds a process based on properties provided. Creates a Proc for
        the parent process.
        :param namedtuple properties: properies of the process to watch
        :return Proc:
        :rtype Proc:
        """
        for proc in psutil.process_iter():
            if cls._is_match(proc, properties):
                # return the parent of this process
                return cls(pid=cls._parent_walk(proc))

    def __unicode__(self):
        return '{}_{}'.format(self.pid(), self.name())

    def __init__(self, pid=None):
        super().__init__(pid=pid)
