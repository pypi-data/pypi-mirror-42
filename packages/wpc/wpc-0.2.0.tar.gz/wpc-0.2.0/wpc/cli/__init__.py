from .customer_cmd import customer  # , remove as client_remove, add as client_add, edit as client_edit, show as client_show

from .config_cmd import config

from .invoice_cmd import invoice

from .work_cmd import work  # , between as work_between, show as work_show, add as work_add, remove as work_remove
# from .work import edit  # as work_edit

from .payment_cmd import payment

from .report_cmd import report

from .cli import cli_commands  # must be last import.


__all__ = ["cli", "customer", "config", "invoice", "work", "payment", "report"
           # "work_add", "work_between", "work_edit", "work_remove", "work_show",
           # "client_add", "client_edit", "client_remove", "client_show"
           ]
pass
