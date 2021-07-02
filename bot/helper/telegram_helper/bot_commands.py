import os

def getCommand(name: str, command: str):
    try:
        if len(os.environ[name]) == 0:
            raise KeyError
        return os.environ[name]
    except KeyError:
        return command
class _BotCommands:
    def __init__(self):
        self.StartCommand = getCommand('START_COMMAND', 'start')
        self.MirrorCommand = getCommand('MIRROR_COMMAND', 'mirror')
        self.UnzipMirrorCommand = getCommand('UNZIP_COMMAND', 'unzipmirror')
        self.TarMirrorCommand = getCommand('TAR_COMMAND', 'tarmirror')
        self.CancelMirror = getCommand('CANCEL_COMMAND', 'cancel')
        self.CancelAllCommand = getCommand('CANCELALL_COMMAND', 'cancelall')
        self.ListCommand = getCommand('LIST_COMMAND', 'list')
        self.SpeedCommand = getCommand('SPEED_COMMAND', 'speedtest')
        self.CountCommand = getCommand('COUNT_COMMAND', 'count')
        self.StatusCommand = getCommand('STATUS_COMMAND', 'status')
        self.AuthorizeCommand = getCommand('AUTH_COMMAND', 'authorize')
        self.UnAuthorizeCommand = getCommand('UNAUTH_COMMAND', 'unauthorize')
        self.PingCommand = getCommand('PING_COMMAND', 'ping')
        self.RestartCommand = getCommand('RESTART_COMMAND', 'restart')
        self.StatsCommand = getCommand('STATS_COMMAND', 'stats')
        self.HelpCommand = getCommand('HELP_COMMAND', 'help')
        self.LogCommand = getCommand('LOG_COMMAND', 'log')
        self.CloneCommand = getCommand('CLONE_COMMAND', 'clone')
        self.WatchCommand = getCommand('WATCH_COMMAND', 'watch')
        self.TarWatchCommand = getCommand('TARWATCH_COMMAND', 'tarwatch')
        self.deleteCommand = getCommand('DELETE_COMMAND', 'del')

BotCommands = _BotCommands()
