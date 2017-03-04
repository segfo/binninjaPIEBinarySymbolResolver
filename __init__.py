from binaryninja import *
import symbolResolver

PluginCommand.register_for_address("SymbolResolver", "Basically does nothing", symbolResolver.resolve)