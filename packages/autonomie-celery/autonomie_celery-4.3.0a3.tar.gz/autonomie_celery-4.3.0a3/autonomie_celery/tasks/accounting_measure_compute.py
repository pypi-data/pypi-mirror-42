# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Tasks used to compile treasury measures
"""
import transaction

from pyramid_celery import celery_app
from sqlalchemy import or_
from autonomie_base.models.base import DBSESSION
from autonomie_base.mail import send_mail
from autonomie.models.accounting.operations import (
    AccountingOperationUpload,
    AccountingOperation,
)
from autonomie.models.accounting.treasury_measures import (
    TreasuryMeasure,
    TreasuryMeasureGrid,
    TreasuryMeasureType,
)
from autonomie_celery.conf import (
    get_recipients_addresses,
)
from autonomie.models.accounting.income_statement_measures import (
    IncomeStatementMeasure,
    IncomeStatementMeasureGrid,
    IncomeStatementMeasureType,
)

from autonomie_celery.tasks import utils


logger = utils.get_logger(__name__)


class BaseMeasureCompiler(object):
    """
    Base measure compiler
    """
    measure_type_class = None
    measure_grid_class = None
    measure_class = None

    def __init__(self, upload, operations):
        self.upload = upload
        self.operations = operations
        self.session = DBSESSION()

        self.measure_types = self._collect_measure_types()

        self.grids = self.collect_existing_grids()
        self.measure_cache = self.collect_existing_measures(self.grids)
        self.measures = {}

    def _collect_measure_types(self):
        return self.measure_type_class.query().filter_by(active=True)

    def get_cache_key_from_grid(self, grid):
        """
        Build a cache key based on the given grid object

        :param obj grid: The grid instance
        :returns: A valid dict key
        """
        pass

    def get_cache_key_from_operation(self, operation):
        """
        Build a cache key based on the given operation object

        :param obj operation: The AccountingOperation instance
        :returns: A valid dict key
        """
        pass

    def collect_existing_measures(self, grids):
        """
        Build the measures dict based on the given existing grids
        Also reset all values to 0

        :param dict grids: The grid cache

        :returns: A cache dict storing existing measures by (company_id, month)
        """
        # Stores built measures {'company1_id': {'measure1_id': object,
        # 'measure2_id': instance}, ...}
        result = {}
        for grid in grids.values():
            cache_key = self.get_cache_key_from_grid(grid)
            company_measures = result[cache_key] = {}
            for measure in grid.measures:
                company_measures[measure.measure_type_id] = measure

        return result

    def get_measures(self, operation):
        """
        Retrieve a measure from the current cache

        :param obj operation: The operation for which we try to set measures
        """
        key = self.get_cache_key_from_operation(operation)
        if key in self.measures:
            # We already retrieved this datas from cache
            result = self.measures[key]
        elif key in self.measure_cache:
            # We retrieve it from the cache the first time (setting values to 0)
            result = self.measures[key] = self.measure_cache[key]
            for measure in result.values():
                measure.value = 0
        else:
            # No existing measure is matching the operation
            result = self.measures[key] = {}
        return result

    def _get_new_measure(self, label, grid_id, measure_type_id=None):
        """
        Build a new measure
        """
        measure = self.measure_class(
            label=label,
            grid_id=grid_id,
            measure_type_id=measure_type_id,
        )
        self.session.add(measure)
        self.session.flush()
        return measure

    def collect_existing_grids(self):
        """
        Collect grids already built on the given upload

        :rtype: dict that should allow to retrieve grid regarding an operation
        """
        # Stores grids : {'company1_id': <TreasuryMeasureGrid>}
        grids = {}
        for grid in self.measure_grid_class.query():
            key = self.get_cache_key_from_grid(grid)
            grids[key] = grid
        return grids

    def get_grid(self, operation):
        """
        Retrieve the grid related to the given operation datas

        :param obj operation: an AccountingOperation instance
        :returns: A Grid instance
        """
        key = self.get_cache_key_from_operation(operation)
        return self.grids.get(key)

    def store_grid(self, new_grid):
        """
        Store a new grid in the grid's cache
        """
        key = self.get_cache_key_from_grid(new_grid)
        self.grids[key] = new_grid

    def process_datas(self):
        """
        Compile measures based on the given operations
        """
        logger.debug(
            u"    + Processing datas with {}".format(self.__class__.__name__)
        )
        for operation in self.operations:
            if operation.company_id is None:
                continue

            grid = self.get_grid(operation)
            if grid is None:
                grid = self._get_new_grid(operation)
                self.store_grid(grid)
                self.session.add(grid)
                self.session.flush()
            else:
                grid.date = self.upload.date
                grid = self.session.merge(grid)

            company_measures = self.get_measures(operation)

            matched = False
            for measure_type in self.measure_types:
                if measure_type.match(operation.general_account):
                    measure = company_measures.get(measure_type.id)
                    if measure is None:
                        measure = self._get_new_measure(
                            measure_type.label,
                            grid.id,
                            measure_type.id
                        )
                        company_measures[measure_type.id] = measure

                    measure.value += operation.total()
                    matched = True

            if matched:
                self.session.merge(measure)

        return self.grids


class TreasuryMeasureCompiler(BaseMeasureCompiler):
    measure_type_class = TreasuryMeasureType
    measure_grid_class = TreasuryMeasureGrid
    measure_class = TreasuryMeasure
    label = u"Génération des états de trésorerie"

    def get_message(self, grids):
        return u"""Génération des états de trésorerie

États de trésorerie générés : {}

----
Autonomie
""".format(len(grids))

    def get_cache_key_from_operation(self, operation):
        """
        Build a cache key based on the given operation object
        """
        return (operation.company_id, self.upload.date)

    def get_cache_key_from_grid(self, grid):
        """
        Build a cache key based on the given grid object
        """
        return (grid.company_id, grid.date)

    def _get_new_grid(self, operation):
        """
        Build a new grid based on the given operation

        :param obj operation: The AccountingOperation from which we build
        measure
        """
        return TreasuryMeasureGrid(
            date=self.upload.date,
            company_id=operation.company_id,
            upload=self.upload,
        )


class IncomeStatementMeasureCompiler(BaseMeasureCompiler):
    measure_type_class = IncomeStatementMeasureType
    measure_grid_class = IncomeStatementMeasureGrid
    measure_class = IncomeStatementMeasure
    label = u"Génération des comptes de résultat"

    def get_message(self, grids):
        return u"""Génération des comptes de résultat :

Comptes de résultat traités : {}

----
Autonomie
""".format(len(grids)/12)

    def _collect_measure_types(self):
        return self.measure_type_class.query(
        ).filter_by(
            active=True
        ).filter(
            or_(
                IncomeStatementMeasureType.is_total == False,  # noqa: E712
                IncomeStatementMeasureType.total_type == 'account_prefix',
            )
        )

    def get_cache_key_from_operation(self, operation):
        """
        Build a cache key based on the given operation object
        """
        return (operation.company_id, operation.date.year, operation.date.month)

    def get_cache_key_from_grid(self, grid):
        """
        Build a cache key based on the given grid object
        """
        return (grid.company_id, grid.year, grid.month)

    def _get_new_grid(self, operation):
        """
        Build a new grid based on the given operation

        :param obj operation: The AccountingOperation from which we build
        measure
        """
        return IncomeStatementMeasureGrid(
            year=operation.date.year,
            month=operation.date.month,
            company_id=operation.company_id,
            upload=self.upload,
        )


def get_measure_compilers(data_type):
    """
    Retrieve the measure compilers to be used with this given type of datas

    :param str data_type: The type of data we build our measures from
    :returns: The measure compiler
    """
    if data_type == AccountingOperationUpload.ANALYTICAL_BALANCE:
        logger.info("  + Handling analytical_balance file")
        return [TreasuryMeasureCompiler]
    elif data_type == AccountingOperationUpload.GENERAL_LEDGER:
        logger.info("  + Handling General Ledger file")
        return [IncomeStatementMeasureCompiler]
    elif data_type == AccountingOperationUpload.SYNCHRONIZED_ACCOUNTING:
        return [TreasuryMeasureCompiler, IncomeStatementMeasureCompiler]

MAIL_ERROR_SUBJECT = u"[Erreur] {}"
MAIL_SUCCESS_SUBJECT = u"[Succès] {}"


def send_success(request, mail_addresses, type_label, message):
    """
    Send a success email

    :param obj request: The current request object
    :param list mail_addresses: List of recipients e-mails
    :param str message: message to send
    """
    if mail_addresses:
        try:
            subject = MAIL_SUCCESS_SUBJECT.format(type_label)
            send_mail(request, mail_addresses, message, subject)
        except:
            logger.exception(u"Error sending email")


def send_error(request, mail_addresses, type_label, message):
    """
    Send an error email

    :param obj request: The current request object
    :param list mail_addresses: List of recipients e-mails
    :param str message: message to send
    """
    if mail_addresses:
        try:
            subject = MAIL_ERROR_SUBJECT.format(type_label)
            send_mail(request, mail_addresses, message, subject)
        except:
            logger.exception(u"Error sending email")


@celery_app.task(bind=True)
def compile_measures_task(self, upload_id):
    """
    Celery task handling measures compilation
    """
    logger.info(
        u"Launching the compile measure task for upload {0}".format(upload_id)
    )
    transaction.begin()
    upload = AccountingOperationUpload.get(upload_id)
    if upload is None:
        raise Exception(
            u"No AccountingOperationUpload instance with id {}".format(
                upload_id
            )
        )
    operations = AccountingOperation.query().filter_by(
        upload_id=upload_id
    ).all()

    mail_addresses = get_recipients_addresses(self.request)
    compiler_factories = get_measure_compilers(upload.filetype)
    messages = []
    for compiler_factory in compiler_factories:
        try:
            compiler = compiler_factory(upload, operations)
            grids = compiler.process_datas()
            messages.append(compiler.get_message(grids))
        except:
            logger.exception(u"Error while generating measures")
            transaction.abort()
            send_error(
                self.request,
                mail_addresses,
                compiler.label,
                compiler.error_message,
            )
            return False
        else:
            logger.info(u"{0} measure grids were handled".format(len(grids)))
            send_success(
                self.request,
                mail_addresses,
                compiler.label,
                compiler.get_message(grids),
            )
            logger.info(
                u"A success email has been sent to {0}".format(
                    mail_addresses
                )
            )

    transaction.commit()
    logger.info(u"The transaction has been commited")
    logger.info(u"* Task SUCCEEDED !!!")
