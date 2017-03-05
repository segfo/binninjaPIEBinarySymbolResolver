from binaryninja import *
import symbolResolver

PluginCommand.register_for_address("SymbolResolver", "", symbolResolver.resolve)
