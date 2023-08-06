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
from collections import OrderedDict

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
    TreasuryMeasureTypeCategory,
)
from autonomie_celery.conf import (
    get_recipients_addresses,
)
from autonomie.models.accounting.income_statement_measures import (
    IncomeStatementMeasure,
    IncomeStatementMeasureGrid,
    IncomeStatementMeasureType,
    IncomeStatementMeasureTypeCategory,
)

from autonomie_celery.tasks import utils


logger = utils.get_logger(__name__)


class GridCacheItem:
    def __init__(self, grid):
        self.grid = grid
        for measure in grid.measures:
            measure.value = 0

        self._measures = dict(
            (measure.measure_type_id, measure) for measure in grid.measures
        )
        self._category_totals = {}
        self._type_totals = {}

    def get_measures(self):
        return self._measures

    def store_measure(self, measure):
        self._measures[measure.measure_type_id] = measure
        if measure not in self.grid.measures:
            self.grid.measures.append(measure)

    def set_total_type(self, measure_type, value):
        self._type_totals[measure_type.id] = value

    def update_category_total(self, measure_type, value):
        if measure_type.category_id not in self._category_totals:
            self._category_totals[measure_type.category_id] = 0
        self._category_totals[measure_type.category_id] += value

    def get_type_total(self, typ_id):
        return self._type_totals.get(typ_id, 0)

    def get_category_total(self, category_id):
        return self._category_totals.get(category_id, 0)


class GridCache:
    """
    A grid cache used to temporarly store all datas related to the current
    computation
    """
    def __init__(self):
        self._datas = {}

    def store_grid(self, key, grid):
        self._datas[key] = GridCacheItem(grid)
        return self._datas[key]

    def get(self, key):
        return self._datas.get(key)


class BaseMeasureCompiler(object):
    """
    Base measure compiler

    Uses a cache to store grids currently edited

    For each grid, the cache contains :

        - Measures already created
        - totals by category
        - totals by type

    Totals are used in a second time to compute "total" measures (not related to
    account numbers)
    """
    measure_type_class = None
    measure_type_category_class = None
    measure_grid_class = None
    measure_class = None

    def __init__(self, upload, operations):
        self.upload = upload
        self.operations = operations
        self.session = DBSESSION()

        self.cache = GridCache()

        # Collect all types
        self.common_measure_types = self._collect_common_measure_types()
        self.categories = self._collect_categories()
        self.computed_measure_types = self._collect_computed_measure_types()

        self.processed_grids = []

    def _get_active_type_query(self):
        """
        Build a query to list active measure types
        :returns: An sqlalchemy query object
        """
        return self.measure_type_class.query(
        ).join(
            self.measure_type_category_class
        ).filter(
            self.measure_type_class.active == True  # noqa: E712
        ).filter(
            self.measure_type_category_class.active == True  # noqa: E712
        )

    def _collect_common_measure_types(self):
        """
        Retrieve measure types that are not computed from other measures
        :returns: The list of measure types
        """
        return self._get_active_type_query().filter(
            or_(
                self.measure_type_class.is_total == False,  # noqa: E712
                self.measure_type_class.total_type == 'account_prefix',
            )
        ).all()

    def _collect_categories(self):
        """
        Retrieve all measure type categories
        """
        return self.measure_type_category_class.get_categories()

    def _collect_computed_measure_types(self):
        """
        Collect computed measure types and store them by category id

        :returns: a dict {category_id: [list of MeasureType]}
        """
        result = OrderedDict()
        query = self._get_active_type_query()
        query = query.filter(
            self.measure_type_class.is_total == True,  # noqa: E712
        ).filter(
            self.measure_type_class.total_type != 'account_prefix',
        ).order_by(
            self.measure_type_category_class.order
        ).order_by(self.measure_type_class.order)
        for typ in query:
            result.setdefault(typ.category_id, []).append(typ)
        return result

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

    def get_grid(self, operation):
        """
        Retrieve the grid related to the given operation datas

        :param obj operation: an AccountingOperation instance
        :returns: A Grid instance
        """
        key = self.get_cache_key_from_operation(operation)
        cached_grid = self.cache.get(key)
        if cached_grid is None:
            grid = self._query_grid(operation)
            if grid is None:
                grid = self._get_new_grid(operation)
                self.session.add(grid)
                self.session.flush()
            cached_grid = self.cache.store_grid(key, grid)
        return cached_grid

    def get_values_for_computation(self, cached_grid):
        """
        Collect total values in a dict for complex datas computation

        :param obj cached_grid: An instance of GridCacheItem
        """
        result = {}
        for category in self.categories:
            result[category.label] = cached_grid.get_category_total(category.id)

        for typ_ in self.common_measure_types:
            result[typ_.label] = cached_grid.get_type_total(typ_.id)

        for typlist_ in self.computed_measure_types.values():
            for typ_ in typlist_:
                value = cached_grid.get_type_total(typ_.id)
                if value:
                    result[typ_.label] = value

        return result

    def _process_common_measures(self):
        """
        Compile common measures (related to an account prefix) with the given
        operations

        :returns: A list of GridCacheItem
        """
        logger.debug(
            u"    + Processing datas with {}".format(self.__class__.__name__)
        )
        for operation in self.operations:
            if operation.company_id is None:
                continue

            current_grid_cache = self.get_grid(operation)
            grid = current_grid_cache.grid
            if current_grid_cache not in self.processed_grids:
                self.processed_grids.append(current_grid_cache)

            measures = current_grid_cache.get_measures()

            matched = False
            for measure_type in self.common_measure_types:
                if measure_type.match(operation.general_account):
                    measure = measures.get(measure_type.id)
                    if measure is None:
                        measure = self._get_new_measure(
                            measure_type.label,
                            grid.id,
                            measure_type.id
                        )
                        current_grid_cache.store_measure(measure)

                    measure.value += operation.total()
                    current_grid_cache.set_total_type(
                        measure_type, measure.value
                    )
                    current_grid_cache.update_category_total(
                        measure_type, measure.value
                    )
                    matched = True

            if matched:
                self.session.merge(measure)
        return self.processed_grids

    def _process_computed_measures(self):
        """
        Process dynamically computed measures (based on the other ones)

        :returns: A list of GridCacheItem
        """
        for cached_grid in self.processed_grids:
            logger.debug(u"Handling a cached grid")
            measures = cached_grid.get_measures()
            logger.debug(u"Cachged grid measures : {}".format(measures))
            logger.debug(self.computed_measure_types)
            for category_id, measure_types in \
                    self.computed_measure_types.items():
                for measure_type in measure_types:
                    values = self.get_values_for_computation(cached_grid)
                    value = measure_type.compute_total(values)
                    cached_grid.set_total_type(measure_type, value)
                    measure = measures.get(measure_type.id)
                    if measure is None:
                        logger.debug(
                            u"Adding a new computed measure for {}".format(
                                measure_type.label,
                            )
                        )
                        measure = self._get_new_measure(
                            measure_type.label,
                            cached_grid.grid.id,
                            measure_type.id
                        )
                        cached_grid.store_measure(measure)

                    measure.value = value
                    self.session.merge(measure)

        return self.processed_grids

    def process_datas(self):
        """
        Main entry point to process measure computation
        """
        self._process_common_measures()
        self.session.flush()
        self._process_computed_measures()
        self.session.flush()
        return [griditem.grid for griditem in self.processed_grids]


class TreasuryMeasureCompiler(BaseMeasureCompiler):
    measure_type_class = TreasuryMeasureType
    measure_type_category_class = TreasuryMeasureTypeCategory
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

    def _query_grid(self, operation):
        """
        Query a grid associated to the given operation

        Query filters should match the get_cache_key_from_operation options
        """
        return TreasuryMeasureGrid.query().filter_by(
            date=self.upload.date
        ).filter_by(company_id=operation.company_id).first()

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
    measure_type_category_class = IncomeStatementMeasureTypeCategory
    measure_grid_class = IncomeStatementMeasureGrid
    measure_class = IncomeStatementMeasure
    label = u"Génération des comptes de résultat"

    def get_message(self, grids):
        return u"""Génération des comptes de résultat :

Comptes de résultat traités : {}

----
Autonomie
""".format(len(grids)/12)

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

    def _query_grid(self, operation):
        """
        Query a grid associated to the given operation

        Query filters should match the get_cache_key_from_operation options
        """
        return IncomeStatementMeasureGrid.query().filter_by(
            year=operation.date.year
        ).filter_by(
            month=operation.date.month
        ).filter_by(company_id=operation.company_id).first()

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
