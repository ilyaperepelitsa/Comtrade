import json
import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import TEXT, VARCHAR, INTEGER
from sqlalchemy.dialects.postgresql import TIMESTAMP, ARRAY
from sqlalchemy import Boolean
from sqlalchemy import desc

from sqlalchemy.sql import select
from sqlalchemy.sql import exists

# import keys
import pkg_resources
json_path = pkg_resources.resource_filename('credentials', 'passwords.json')

# root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# json_path = os.path.join(root_path, "credentials/passwords.json")

data = json.load(open(json_path))


def inst_to_dict(inst, delete_id=True):
    dat = {}
    for column in inst.__table__.columns:
        dat[column.name] = getattr(inst, column.name)
    # if delete_id:
    #     dat.pop("num")
    return dat

def get_entry_id(entry, session, item, item_column,
                    query_string, target_column_string):
    entry_exists = session.query(exists().where(
        item_column == query_string)).scalar()

    if not entry_exists:
        adding_item = item(**entry)
        session.add(adding_item)
        session.commit()

    item_query = session.query(item).filter(
        item_column == query_string).one()
    query_result = inst_to_dict(item_query)[target_column_string]
    entry_id = query_result

    return entry_id

def post_entry(entry, session, item, item_column, query_string):
    entry_exists = session.query(exists().where(
        item_column == query_string)).scalar()

    if not entry_exists:
        adding_item = item(**entry)
        session.add(adding_item)
        session.commit()
    else:
        pass


def get_id(session, item, item_column,
                query_string, target_column_string):
    entry_exists = session.query(exists().where(
        item_column == query_string)).scalar()

    if entry_exists:
        item_query = session.query(item).filter(
            item_column == query_string).one()
        query_result = inst_to_dict(item_query)[target_column_string]
        return query_result
    else:
        ask_again = input("The '%s' didn't work, try again. Type 'stop' to stop." % query_string)
        return get_id(session, item, item_column,
                        ask_again, target_column_string, error_string)

def delete_label(session, item, item_column,
                query_string, target_column_string,
                item2, item2_column, target2_column_string):
    label_exists = session.query(exists().where(
        item_column == query_string)).scalar()

    if label_exists:
        item_query = session.query(item).filter(
            item_column == query_string).one()
        query_result = inst_to_dict(item_query)[target_column_string]

    session.query(item2).\
        filter(item2_column == query_result).\
        update({target2_column_string: None})
    session.commit()

    session.query(item).filter(item_column == query_string).delete()
    session.commit()


# json.loads(s)


dataslap_postgres = data["aws"]["personal"]["dataslap"]["postgres"]["free_20gb"]["dataslap_user"]
# dataslap_postgres = keys.get_dataslap_postgres()


engine_test = create_engine('postgres://%(username)s:%(password)s@%(host)s:%(port)s/comtrade' %
                            {"username": dataslap_postgres["username"],
                             "password": dataslap_postgres["password"],
                             "host": dataslap_postgres["host"],
                             "port": dataslap_postgres["port"]})
Base_item = declarative_base()


class Reporter(Base_item):
    __tablename__ = "reporters"
    id = Column(INTEGER, primary_key=True)
    reporter_name = Column(TEXT, unique=True)

    def __repr__(self):
        return "<Reporter(id='%s', reporter_name='%s')>"\
            % (self.id, self.reporter_name)

class Reporter_ISO(Base_item):
    __tablename__ = "reporter_iso"
    id = Column(INTEGER, primary_key=True)
    iso_code = Column(TEXT, unique=True)

    def __repr__(self):
        return "<Reporter_ISO(id='%s', iso_code='%s')>"\
            % (self.id, self.iso_code)

class Partner(Base_item):
    __tablename__ = "partners"
    id = Column(INTEGER, primary_key=True)
    partner_name = Column(TEXT, unique=True)

    def __repr__(self):
        return "<Partner(id='%s', partner_name='%s')>"\
            % (self.id, self.partner_name)

class Partner_ISO(Base_item):
    __tablename__ = "partner_iso"
    id = Column(INTEGER, primary_key=True)
    iso_code = Column(TEXT, unique=True)

    def __repr__(self):
        return "<Partner_ISO(id='%s', iso_code='%s')>"\
            % (self.id, self.iso_code)

class Trade_regimes(Base_item):
    __tablename__ = "trade_regimes"
    id = Column(INTEGER, primary_key=True)
    trade_regime_name = Column(TEXT, unique=True)

    def __repr__(self):
        return "<Trade_regime(id='%s', trade_regime_name='%s')>"\
            % (self.id, self.trade_regime_name)


class Commodity_code_EN(Base_item):
    __tablename__ = "commodity_codes_en"
    id = Column(String(6), primary_key=True)
    commodity_name = Column(TEXT, unique=False)

    def __repr__(self):
        return "<Commodity_code_EN(id='%s', commodity_name='%s')>"\
            % (self.id, self.commodity_name)

class Commodity_code_RU(Base_item):
    __tablename__ = "commodity_codes_ru"
    id = Column(String(6), primary_key=True)
    commodity_name = Column(TEXT, unique=False)
    product_group = Column(TEXT, unique=False)

    def __repr__(self):
        return "<Commodity_code_EN(id='%s', commodity_name='%s', product_group='%s')>"\
            % (self.id, self.commodity_name, self.product_group)


class Quantity_code(Base_item):
    __tablename__ = "quantity_codes"
    id = Column(INTEGER, primary_key=True)
    quantity_name = Column(TEXT, unique=True)

    def __repr__(self):
        return "<Quantity_code(id='%s', quantity_name='%s')>"\
            % (self.id, self.quantity_name)



class Trade_aggregation_entry(Base_item):
    __tablename__ = "trade_aggregation_entries"
    id = Column(INTEGER, primary_key=True)

    pf_code = Column(String(6), unique=False)

    year = Column(Integer)
    period = Column(Integer)
    period_description = Column(TEXT)

    aggregation_level = Column(Integer)

    trade_regime = Column(INTEGER, ForeignKey("trade_regimes.id"), nullable=False)
    reporter = Column(INTEGER, ForeignKey("reporters.id"), nullable=False)
    partner = Column(INTEGER, ForeignKey("partners.id"), nullable=False)
    commodity = Column(String(6), ForeignKey("commodity_codes_en.id"), nullable=False)
    quantity_code = Column(INTEGER, ForeignKey("quantity_codes.id"), nullable=False)

    trade_quantity = Column(Integer)
    net_weight = Column(Integer)
    trade_value = Column(Integer)


    def __repr__(self):
        return "<Trade_aggregation_entry(id='%s', pf_code='%s', year='%s', period='%s',\
                    period_description='%s', aggregation_level='%s', trade_regime='%s',\
                    reporter='%s', partner='%s', commodity='%s',\
                    quantity_code='%s', trade_quantity='%s',\
                    net_weight='%s', trade_value='%s')>"\
        % (self.id, self.pf_code, self.year, self.period, self.period_description, self.aggregation_level,
            self.trade_regime, self.reporter, self.partner, self.commodity,
            self.quantity_code, self.trade_quantity, self.net_weight, self.trade_value)


Base_item.metadata.create_all(engine_test)
Session_test = sessionmaker(bind=engine_test)
session_test = Session_test()
