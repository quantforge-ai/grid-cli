"""
Grid CLI - Command Handlers Mapping
"""

from grid.shell import handlers_logic

def get_handler(cmd):
    mapping = {
        "dev": handlers_logic.handle_dev,
        "init": handlers_logic.handle_init,
        "eject": handlers_logic.handle_eject,
        "submit": handlers_logic.handle_submit,
        "roast": handlers_logic.handle_roast,
        "undo": handlers_logic.handle_undo,
        "targets": handlers_logic.handle_targets,
        "check": handlers_logic.handle_check,
        "run": handlers_logic.handle_run,
        "purge": handlers_logic.handle_purge,
        "status": handlers_logic.handle_status,
        "login": handlers_logic.handle_login,
        # Developer Utilities
        "coin": handlers_logic.handle_coin,
        "zen": handlers_logic.handle_zen,
        "blame": handlers_logic.handle_blame,
        # Delegated Intelligence
        "train": lambda args: handlers_logic.handle_delegated("train", args),
        "push": lambda args: handlers_logic.handle_delegated("push", args),
        "pull": lambda args: handlers_logic.handle_delegated("pull", args),
        "upgrade": handlers_logic.handle_upgrade,
    }
    
    # Allow some intelligence delegation directly
    if cmd in mapping:
        handler = mapping[cmd]
        if cmd in ["train", "push", "pull"]:
            # This block is now redundant because "train", "push", "pull" are already lambdas
            # in the mapping, but keeping it as per original logic structure.
            return lambda args: handler(cmd, args)
        return handler
    
    return None
