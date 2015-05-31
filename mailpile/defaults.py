APPVER = "0.4.4"
ABOUT = """\
Mailpile.py          a tool                 Copyright 2013-2014, Mailpile ehf
               for searching and                   <https://www.mailpile.is/>
           organizing piles of e-mail

This program is free software: you can redistribute it and/or modify it under
the terms of either the GNU Affero General Public License as published by the
Free Software Foundation or the Apache License 2.0 as published by the Apache
Software Foundation. See the file COPYING.md for details.
"""
#############################################################################
import os
import time

from mailpile.config import PathDict
from mailpile.config import ConfigRule as c
from mailpile.config import CriticalConfigRule as X
from mailpile.config import PublicConfigRule as p
from mailpile.config import KeyConfigRule as k


_ = lambda string: string


DEFAULT_SENDMAIL = '|/usr/sbin/sendmail -i %(rcpt)s'
CONFIG_PLUGINS = []
CONFIG_RULES = {
    'version': [_('Mailpile program version'), False, APPVER],
    'homedir': [_('Location of Mailpile data'), False, '(unset)'],
    'timestamp': [_('Configuration timestamp'), int, int(time.time())],
    'master_key': k(_('Master symmetric encryption key'), str, ''),
    'sys': p(_('Technical system settings'), False, {
        'fd_cache_size':  (_('Max files kept open at once'), int,         500),
        'history_length': (_('History length (lines, <0=no save)'), int,  100),
        'http_host':     p(_('Listening host for web UI'),
                           'hostname', 'localhost'),
        'http_port':     p(_('Listening port for web UI'), int,         33411),
        'http_path':     p(_('HTTP path of web UI'), 'webroot',            ''),
        'postinglist_kb': (_('Posting list target size in KB'), int,       64),
        'sort_max':       (_('Max results we sort "well"'), int,         2500),
        'snippet_max':    (_('Max length of metadata snippets'), int,     250),
        'debug':         p(_('Debugging flags'), str,                      ''),
        'gpg_keyserver':  (_('Host:port of PGP keyserver'),
                           str, 'pool.sks-keyservers.net'),
        'gpg_home':      p(_('Override the home directory of GnuPG'), 'dir',
                           None),
        'local_mailbox_id': (_('Local read/write Maildir'), 'b36',         ''),
        'mailindex_file': (_('Metadata index file'), 'file',               ''),
        'postinglist_dir': (_('Search index directory'), 'dir',            ''),
        'mailbox':        [_('Mailboxes we index'), 'bin',                 []],
        'plugins':        [_('Plugins to load on startup'),
                           CONFIG_PLUGINS, []],
        'path':           [_('Locations of assorted data'), False, {
            'html_theme': [_('Default theme'),
                           'dir', os.path.join('mailpile', 'www', 'default')],
            'vcards':     [_('Location of vcards'), 'dir', 'vcards'],
            'event_log':  [_('Location of event log'), 'dir', 'logs'],
        }],
        'lockdown':       [_('Demo mode, disallow changes'), bool,      False],
        'login_banner':   [_('A custom banner for the login page'), str,   ''],
        'proxy':          [_('Proxy settings'), False, {
            'protocol':   (_('Proxy protocol'),
                           ["tor", "socks5", "socks4", "http", "none"],
                           'none'),
            'fallback':   (_('Allow fallback to direct conns'), bool, False),
            'username':   (_('User name'), str, ''),
            'password':   (_('Password'), str, ''),
            'host':       (_('Host'), str, ''),
            'port':       (_('Port'), int, 8080)
        }],
    }),
    'prefs': p(_("User preferences"), False, {
        'num_results':     (_('Search results per page'), int,             20),
        'rescan_interval': (_('New mail check frequency'), int,           900),
        'open_in_browser':p(_('Open in browser on startup'), bool,       True),
        'gpg_clearsign':  X(_('Inline PGP signatures or attached'),
                            bool, False),
        'gpg_recipient':  p(_('Encrypt local data to ...'), 'gpgkeyid',    ''),
        'gpg_email_key':  (_('Attach public key to outgoing messages?'),
                            bool, True),
        'openpgp_header': X(_('Advertise GPG preferences in a header?'),
                            ['', 'sign', 'encrypt', 'signencrypt'],
                            'signencrypt'),
        'crypto_policy':  X(_('Default encryption policy for outgoing mail'),
                            str, 'none'),
        'inline_pgp':      (_('Use inline PGP when possible'), bool,     True),
        'default_order':   (_('Default sort order'), str,          'rev-date'),
        'obfuscate_index': X(_('Key to use to scramble the index'), str,    ''),
        'index_encrypted': X(_('Make encrypted content searchable'),
                             bool, False),
        'encrypt_mail':   X(_('Encrypt locally stored mail'), bool,      True),
        'encrypt_index':  X(_('Encrypt the local search index'), bool,  False),
        'encrypt_vcards': X(_('Encrypt the contact database'), bool,     True),
        'encrypt_events': X(_('Encrypt the event log'), bool,            True),
        'encrypt_misc':   X(_('Encrypt misc. local data'), bool,         True),
        'rescan_command':  (_('Command run before rescanning'), str,       ''),
        'default_email':   (_('Default outgoing e-mail address'), 'email', ''),
        'default_route':   (_('Default outgoing mail route'), str, ''),
        'always_bcc_self': (_('Always BCC self on outgoing mail'), bool, True),
        'default_messageroute': (_('Default outgoing mail route'), str,    ''),
        'language':       p(_('User interface language'), str,             ''),
        'vcard':           [_("VCard import/export settings"), False, {
            'importers':   [_("VCard import settings"), False,             {}],
            'exporters':   [_("VCard export settings"), False,             {}],
            'context':     [_("VCard context helper settings"), False,     {}],
        }],
    }),
    'web': (_("Web Interface Preferences"), False, {
        'setup_complete':  (_('User completed setup experience'), bool, False),
        'display_density': (_('Display density of interface'), str, 'comfy'),
        'quoted_reply':    (_('Quote replies to messages'), str, 'unset'),
        'nag_backup_key':  (_('Nag user to backup their key'), int, 0),
        'subtags_collapsed': (_('Collapsed subtags in sidebar'), str, []),
        'donate_visibility': (_('Hide donate link in topbar'), bool, True)
    }),
    'logins': [_('Credentials allowed to access Mailpile'), {
        'password':        (_('Salted and hashed password'), str, '')
    }, {}],
    'routes': [_('Outgoing message routes'), {
        'name':            (_('Route name'), str, ''),
        'protocol':        (_('Messaging protocol'),
                            ["smtp", "smtptls", "smtpssl", "local"],
                            'smtp'),
        'username':        (_('User name'), str, ''),
        'password':        (_('Password'), str, ''),
        'command':         (_('Shell command'), str, ''),
        'host':            (_('Host'), str, ''),
        'port':            (_('Port'), int, 587)
    }, {}],
    'sources': [_('Incoming message sources'), {
        'name':            (_('Source name'), str, ''),
        'enabled':         (_('Is this mail source enabled?'), bool, True),
        'protocol':        (_('Mailbox protocol or format'),
                            ["mbox", "maildir", "macmaildir", "gmvault",
                             "imap", "imap_ssl", "pop3", "pop3_ssl"],
                            ''),
        'pre_command':     (_('Shell command run before syncing'), str, ''),
        'post_command':    (_('Shell command run after syncing'), str, ''),
        'interval':        (_('How frequently to check for mail'), int, 300),
        'username':        (_('User name'), str, ''),
        'password':        (_('Password'), str, ''),
        'host':            (_('Host'), str, ''),
        'port':            (_('Port'), int, 993),
        'keepalive':       (_('Keep server connections alive'), bool, False),
        'discovery':       (_('Mailbox discovery policy'), False, {
            'paths':       (_('Paths to watch for new mailboxes'), 'bin', []),
            'policy':      (_('Default mailbox policy'),
                            ['unknown', 'ignore', 'watch',
                             'read', 'move', 'sync'], 'unknown'),
            'local_copy':  (_('Copy mail to a local mailbox?'), bool, False),
            'parent_tag':  (_('Parent tag for mailbox tags'), str, '!CREATE'),
            'guess_tags':  (_('Guess which local tags match'), bool, True),
            'create_tag':  (_('Create a tag for each mailbox?'), bool, True),
            'process_new': (_('Is a potential source of new mail'), bool, True),
            'apply_tags':  (_('Tags applied to messages'), str, []),
        }),
        'mailbox': (_('Mailboxes'), {
            'name':        (_('The name of this mailbox'), str, ''),
            'path':        (_('Mailbox source path'), str, ''),
            'policy':      (_('Mailbox policy'),
                            ['unknown', 'ignore', 'read', 'move', 'sync'],
                            'ignore'),
            'local':       (_('Local mailbox path'), 'bin', ''),
            'process_new': (_('Is a source of new mail'), bool, True),
            'primary_tag': (_('A tag representing this mailbox'), str, ''),
            'apply_tags':  (_('Tags applied to messages'), str, []),
        }, {})
    }, {}],

    ### OLD CRAP, JUST HERE SO AS NOT TO KILL CONFIG FILES
    'profiles': [_('DEPRECATED: User profiles and personalities'), {
        'name':            (_('Account name'), 'str', ''),
        'email':           (_('E-mail address'), 'email', ''),
        'signature':       (_('Message signature'), 'multiline', ''),
        'route':           (_('DEPRECATED, DO NOT USE'), str, ''),
        'messageroute':    (_('Outgoing mail route'), str, ''),
    }, []]
}


if __name__ == "__main__":
    import mailpile.defaults
    from mailpile.config import ConfigDict

    print '%s' % (ConfigDict(_name='mailpile',
                             _comment='Base configuration',
                             _rules=mailpile.defaults.CONFIG_RULES
                             ).as_config_bytes(), )
