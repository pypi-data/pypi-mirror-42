# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from email.header import Header
from email.utils import formataddr, getaddresses

from trytond.config import config
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Eval, Bool
from trytond.report import get_email
from trytond.sendmail import sendmail_transactional, SMTPDataManager
from trytond.transaction import Transaction
from trytond.wizard import StateTransition

__all__ = ['DunningLevel', 'ProcessDunning', 'Dunning', 'DunningEmailLog']


class DunningLevel:
    __metaclass__ = PoolMeta
    __name__ = 'account.dunning.level'
    send_email = fields.Boolean("Send Email")
    email_template = fields.Many2One(
        'ir.action.report', "Email Template",
        domain=[
            ('template_extension', 'in', ['plain', 'html', 'xhtml']),
            ('model', '=', 'account.dunning'),
            ],
        states={
            'required': Bool(Eval('send_email')),
            'invisible': ~Eval('send_email'),
            },
        depends=['send_email'])
    email_from = fields.Char(
        "From",
        states={
            'invisible': ~Eval('send_email'),
            },
        depends=['send_email'],
        help="Leave empty for the value defined in the configuration file.")

    @classmethod
    def default_email_template(cls):
        pool = Pool()
        Data = pool.get('ir.model.data')
        try:
            return Data.get_id('account_dunning_email', 'report_email')
        except KeyError:
            return


class ProcessDunning:
    __metaclass__ = PoolMeta
    __name__ = 'account.dunning.process'
    send_email = StateTransition()

    @classmethod
    def __setup__(cls):
        super(ProcessDunning, cls).__setup__()
        cls._actions.append('send_email')

    def transition_send_email(self):
        pool = Pool()
        Dunning = pool.get('account.dunning')
        Log = pool.get('account.dunning.email.log')
        datamanager = SMTPDataManager()
        if not pool.test:
            Transaction().join(datamanager)
        dunnings = Dunning.browse(Transaction().context['active_ids'])
        logs = []
        for dunning in dunnings:
            if dunning.level.send_email:
                log = dunning.send_email(datamanager=datamanager)
                if log:
                    logs.append(log)
        if logs:
            Log.create(logs)
        return self.next_state('send_email')


class Dunning:
    __metaclass__ = PoolMeta
    __name__ = 'account.dunning'

    def send_email(self, datamanager=None):
        pool = Pool()
        Configuration = pool.get('ir.configuration')
        Lang = pool.get('ir.lang')

        from_ = self.level.email_from or config.get('email', 'from')
        to = []
        if self.party.email:
            name = str(Header(self.party.rec_name))
            to.append(formataddr((name, self.party.email)))
        cc = []
        bcc = []
        languages = set()
        if self.party.lang:
            languages.add(self.party.lang)
        else:
            lang, = Lang.search([
                    ('code', '=', Configuration.get_language()),
                    ], limit=1)
            languages.add(lang)

        msg = self._email(from_, to, cc, bcc, languages)
        to_addrs = [e for _, e in getaddresses(to + cc + bcc)]
        if to_addrs:
            if not pool.test:
                sendmail_transactional(
                    from_, to_addrs, msg, datamanager=datamanager)
            return self._email_log(msg)

    def _email(self, from_, to, cc, bcc, languages):
        # TODO order languages to get default as last one for title
        msg, title = get_email(self.level.email_template, self, languages)
        msg['From'] = from_
        msg['To'] = ', '.join(to)
        msg['Cc'] = ', '.join(cc)
        msg['Bcc'] = ', '.join(bcc)
        msg['Subject'] = Header(title, 'utf-8')
        msg['Auto-Submitted'] = 'auto-generated'
        return msg

    def _email_log(self, msg):
        return {
            'recipients': msg['To'],
            'recipients_secondary': msg['Cc'],
            'recipients_hidden': msg['Bcc'],
            'dunning': self.id,
            'level': self.level.id,
            }


class DunningEmailLog(ModelSQL, ModelView):
    "Dunning Email Log"
    __name__ = 'account.dunning.email.log'
    date = fields.Function(fields.DateTime("Date"), 'get_date')
    recipients = fields.Char("Recipients")
    recipients_secondary = fields.Char("Secondary Recipients")
    recipients_hidden = fields.Char("Hidden Recipients")
    dunning = fields.Many2One('account.dunning', "Dunning", required=True)
    level = fields.Many2One('account.dunning.level', "Level", required=True)

    def get_date(self, name):
        return self.create_date.replace(microsecond=0)

    @classmethod
    def search_date(cls, name, clause):
        return [('create_date',) + tuple(clause[1:])]

    @staticmethod
    def order_date(tables):
        table, _ = tables[None]
        return [table.create_date]
