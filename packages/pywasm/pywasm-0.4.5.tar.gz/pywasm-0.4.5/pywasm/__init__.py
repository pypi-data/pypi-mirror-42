import typing

from pywasm import convention
from pywasm import execution
from pywasm import log
from pywasm import structure


class VirtualMachine:
    def __init__(self, module: structure.Module, imps: typing.Dict):
        self.module = module
        self.module_instance = execution.ModuleInstance()
        self.store = execution.Store()
        externvals = []
        for e in self.module.imports:
            if e.module not in imps or e.name not in imps[e.module]:
                raise Exception(f'pywasm: global import {e.module}.{e.name} not found')
            if e.kind == convention.extern_func:
                a = execution.HostFunc(self.module.types[e.desc], imps[e.module][e.name])
                self.store.funcs.append(a)
                externvals.append(execution.ExternValue(e.kind, len(self.store.funcs) - 1))
                continue
            if e.kind == convention.extern_table:
                raise NotImplementedError
            if e.kind == convention.extern_mem:
                raise NotImplementedError
            if e.kind == convention.extern_global:
                a = execution.GlobalInstance(execution.Value(e.desc.valtype, imps[e.module][e.name]), e.desc.mut)
                self.store.globals.append(a)
                externvals.append(execution.ExternValue(e.kind, len(self.store.globals) - 1))
                continue
        self.module_instance.instantiate(self.module, self.store, externvals)

    def func_addr(self, name: str):
        for e in self.module_instance.exports:
            if e.name == name and e.value.extern_type == convention.extern_func:
                return e.value.addr
        raise Exception('pywasm: function not found')

    def exec(self, name: str, args: typing.List):
        func_addr = self.func_addr(name)
        func = self.store.funcs[self.module_instance.funcaddrs[func_addr]]
        for i, e in enumerate(func.functype.args):
            if e in [convention.i32, convention.i64]:
                assert isinstance(args[i], int)
            if e in [convention.f32, convention.f64]:
                assert isinstance(args[i], float)
            args[i] = execution.Value(e, args[i])
        stack = execution.Stack()
        stack.ext(args)
        frame = execution.Frame(self.module_instance, args, len(func.functype.rets), -1)
        log.debugln(f'Running function {name}({", ".join([str(e) for e in args])}):')
        r = execution.call(self.module_instance, func_addr, self.store, stack)
        if r:
            return r[0].n
        return None


# Using the pywasm API.
# If you have already compiled a module from another language using tools like Emscripten, or loaded and run the code
# by Javascript yourself, the pywasm API is easy to learn.

def on_debug():
    log.lvl = 1


def load(name: str, imps: typing.Dict = None):
    imps = imps if imps else {}
    with open(name, 'rb') as f:
        module = structure.Module.from_reader(f)
        return VirtualMachine(module, imps)


Memory = execution.MemoryInstance
Value = execution.Value
Table = execution.TableInstance
Limits = structure.Limits
