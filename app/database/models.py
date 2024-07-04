from sqlalchemy import create_engine, Column, String, Integer, Numeric, Boolean, TIMESTAMP, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class TempParams(Base):
    __tablename__ = 'temperature_params'
    idtparam = Column('id_temp_param',Integer, primary_key=True)
    t2temp = Column('t2_total_temp', Numeric)
    t24temp = Column('t24_total_temp', Numeric)
    t30temp = Column('t30_total_temp', Numeric)
    t50temp = Column('t50_total_temp', Numeric)

class PresParams(Base):
    __tablename__ = 'pressure_params'
    idpparam = Column('id_pres_param', Integer, primary_key=True)
    p2pres = Column('p2_total_temp',Numeric)
    p15pres = Column('p15_total_temp', Numeric)
    p30pres = Column('p30_total_temp', Numeric)
    ps30pres = Column('ps30_total_temp', Numeric)

class FlowParams(Base):
    __tablename__ = 'flow_params'
    idfparam = Column('id_flow_param', Integer, primary_key=True)
    w31bleed = Column('w31_cl_bleed', Numeric)
    w32bleed = Column('w32_cl_bleed', Numeric)
    htbleed = Column('ht_bleed_enthalpy', Integer)

class RpmParams(Base):
    __tablename__ = 'rpm_params'
    idrparam = Column('id_rpm_param', Integer, primary_key=True)
    nfrpm = Column('nf_phys_rpm', Numeric)
    ncrpm = Column('nc_phys_rpm', Numeric)
    nrfrpm = Column('nrf_corr_rpm', Numeric)
    nrcrpm = Column('nrc_corr_rpm', Numeric)
    nfdrpm = Column('nrc_dem_rpm', Numeric)
    pcnfr = Column('pcnrf_dem_rpm', Numeric)

class RatioParams(Base):
    __tablename__ = 'ratio_params'
    idrtparam = Column('id_ratio_param', Integer, primary_key=True)
    epr = Column('epr_pres_ratio', Numeric)
    phi = Column('phi_fuel_flow_ratio', Numeric)
    bpr = Column('bpr_bypass_ratio', Numeric)
    farb = Column('farb_burner_air_ratio', Numeric)

class GeneralParams(Base):
    __tablename__ = 'general_params'
    idparam = Column('id_param', Integer, primary_key=True)
    tcycle = Column('time_cycles', Integer)
    idtparam = Column('id_temp_param', Integer, ForeignKey('temperature_params.id_temp_param'), unique=True)
    idpparam = Column('id_pres_param', Integer, ForeignKey('pressure_params.id_pres_param'), unique=True)
    idfparam  = Column('id_flow_param', Integer, ForeignKey('flow_params.id_flow_param'), unique=True)
    idrparam = Column('id_rpm_param', Integer, ForeignKey('rpm_params.id_rpm_param'), unique=True)
    idrtparam = Column('id_ratio_param', Integer, ForeignKey('ratio_params.id_ratio_param'), unique=True)
    idengine = Column('id_engine', Integer, ForeignKey('engine.id_engine'))

class Engine(Base):
    __tablename__ = 'engine'
    __table_args__ = (ForeignKeyConstraint(['manufacturer', 'model'], ['documents.manufacturer','documents.model']), None)
    idengine = Column('id_engine', Integer, primary_key=True)
    nservice = Column('needs_service', Boolean)
    calc_rul = Column('rul', Numeric)
    manufacturer = Column('manufacturer', String)
    model = Column('model', String)

class Service(Base):
    __tablename__ = 'service'
    idservice = Column('id_service', Integer, primary_key=True)
    commentary = Column('commentary', String)
    servdate = Column('service_date', TIMESTAMP)
    idengine = Column('id_engine', Integer, ForeignKey('engine.id_engine'))

class Documents(Base):
    __tablename__ = "documents"
    manufacturer = Column('manufacturer', String, primary_key=True)
    model = Column('model', String, primary_key=True)
    doc_name = Column('doc_name', String)

db_params = {
    'host': 'localhost',
    'database': 'rul_db_n',
    'user': 'postgres',
    'password': '1234'
}

engine = create_engine(
    f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}@{db_params['host']}/{db_params['database']}")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def get_db():
    db_session_local = Session()
    try:
        yield db_session_local
    finally:
        db_session_local.close()
