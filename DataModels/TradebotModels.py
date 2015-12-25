from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, desc
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

class User(Base):
	__tablename__ = 'user'
	user_id = Column(String(13), primary_key = True)
	title = Column(String(50))
	flair_ind = Column(String(1))
	update_dtm = Column(DateTime, default = datetime.datetime.utcnow().strftime(TIME_FORMAT))

	sales = relationship("Trade", foreign_keys = "Trade.seller_id", order_by = "desc(Trade.update_dtm)")
	purchases = relationship("Trade", foreign_keys = "Trade.buyer_id", order_by = "desc(Trade.update_dtm)")

	def __eq__(self, other):
		return self.user_id == other.user_id

class Trade(Base):
	__tablename__ = 'trade'
	submission_id = Column(String(6), primary_key = True)
	comment_id = Column(String(7), primary_key = True)
	seller_id = Column(String(20), ForeignKey(User.user_id))
	buyer_id = Column(String(20), ForeignKey(User.user_id))
	item = Column(String(30), nullable = False)
	insurance = Column(String(5))
	amount = Column(Numeric(precision = 7, scale = 2))
	currency = Column(String(3))
	sale_link = Column(String(255))
	comment_link = Column(String(255))
	update_dtm = Column(DateTime, default = datetime.datetime.utcnow().strftime(TIME_FORMAT))

