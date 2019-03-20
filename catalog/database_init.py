from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from Data_Setup import *

engine = create_engine('sqlite:///chipset.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Delete SOC Name if exisitng.
session.query(SocCompany).delete()
# Delete Chipset Name if exisitng.
session.query(SocName).delete()
# Delete User if exisitng.
session.query(User).delete()

# Create sample users data
User1 = User(name="sai praveen",
             email="sai536711@gmail.com")

session.add(User1)
session.commit()
print ("Successfully Add First User")
# Create sample SOC Companies
Company1 = SocCompany(name="QUALCOM SNAPDRAGON",
                      user_id=1)
session.add(Company1)
session.commit()

Company2 = SocCompany(name="HILISILICON KIRIN",
                      user_id=1)
session.add(Company2)
session.commit

Company3 = SocCompany(name="MEDIATEK",
                      user_id=1)
session.add(Company3)
session.commit()

Company4 = SocCompany(name="APPLE BIONIC",
                      user_id=1)
session.add(Company4)
session.commit()

Company5 = SocCompany(name="SAMSUNG EXYNOS",
                      user_id=1)
session.add(Company5)
session.commit()

Company6 = SocCompany(name="INTEL",
                      user_id=1)
session.add(Company6)
session.commit()

# Populare a Chipsets
# Using different users for Chipsets
Chipset1 = SocName(name="snapdragon 845",
                   build="10nm",
                   cores="octa core",
                   frequency="2.8Ghz",
                   date=datetime.datetime.now(),
                   soccompanyid=1,
                   user_id=1)
session.add(Chipset1)
session.commit()

Chipset2 = SocName(name="kirin 980",
                   build="7nm ",
                   cores="octa core",
                   frequency="2.6Ghz",
                   date=datetime.datetime.now(),
                   soccompanyid=2,
                   user_id=1)
session.add(Chipset2)
session.commit()

Chipset3 = SocName(name="helio p70",
                   build="12nm",
                   cores="octa core",
                   frequency="2.1Ghz",
                   date=datetime.datetime.now(),
                   soccompanyid=3,
                   user_id=1)
session.add(Chipset3)
session.commit()

Chipset4 = SocName(name="apple A12 bionic",
                   build="7nm",
                   cores="octa core",
                   frequency="2.4Ghz",
                   date=datetime.datetime.now(),
                   soccompanyid=4,
                   user_id=1)
session.add(Chipset4)
session.commit()

Chipset5 = SocName(name="exynos 9820",
                   build="10nm",
                   cores="octa core",
                   frequency="2.4Ghz",
                   date=datetime.datetime.now(),
                   soccompanyid=5,
                   user_id=1)
session.add(Chipset5)
session.commit()

Chipset6 = SocName(name="X5",
                   build="14nm",
                   cores="quad core",
                   frequency="1.4Ghz",
                   date=datetime.datetime.now(),
                   soccompanyid=6,
                   user_id=1)
session.add(Chipset6)
session.commit()

print("Your database has been inserted!")
