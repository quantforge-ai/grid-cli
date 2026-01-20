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
        "undo": handlers_logic.handle_undo,
        "roast": handlers_logic.handle_roast,
        "run": handlers_logic.handle_run,
        "targets": handlers_logic.handle_targets,
        "check": handlers_logic.handle_check,
        "train": handlers_logic.handle_delegated,
        "push": handlers_logic.handle_delegated,
        "pull": handlers_logic.handle_delegated,
        "login": handlers_logic.handle_login,
        "status": handlers_logic.handle_status,
        "purge": handlers_logic.handle_purge,
        "upgrade": handlers_logic.handle_upgrade,
    }
    
    # Allow some intelligence delegation directly
    if cmd in mapping:
        handler = mapping[cmd]
        if cmd in ["train", "push", "pull"]:
            return lambda args: handler(cmd, args)
        return handler
    
    return None
