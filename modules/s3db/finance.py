__all__ = ["FinanceDonations",
           "IncomeType",
		   "IncomeDetails",
		   "Income"
           ]

from gluon import *
from gluon.storage import Storage
from ..s3 import *
from s3layouts import S3AddResourceLink


class FinanceDonations(S3Model):
	names = ["finance_donations",
             "finance_donations_id",
			 
			 ]
			 
	def model(self):

        # You will most likely need (at least) these:
			db = current.db
			T = current.T

        # This one may be useful:
			settings = current.deployment_settings
	

			tablename = "finance_donations"
			table=self.define_table(tablename,
							Field("donar", label=T("Donar"),),
							Field("amount", "integer", label=T("Amount"),
									#default=0.00, 
									#requires = IS_FLOAT_AMOUNT(),
									),
							s3_currency(required=True),
							)
			
			self.configure(tablename,
						   listadd=True,
						   realm_components = ("incomedetails"))
						   
			finance_donations_id = S3ReusableField("finance_donations_id", table,
                                               label = T("Finance Donations"),
                                               requires = IS_NULL_OR(IS_ONE_OF(db,
                                                                     "finance_donations.id")))
																	 
			

																	 
			# Pass names back to global scope (s3.*)
			return dict(
				finance_donations_id=finance_donations_id,
			)
	
#==============================================================================================================================

class IncomeType(S3Model):

	names = ["finance_incometype",
			"finance_incometype_id",
			]
	
	def model(self):
		db = current.db
		T = current.T
		settings = current.deployment_settings
	
		
		tablename = "finance_incometype"
		table=self.define_table(tablename,
								Field("name", label=T("Name")),
								#Field.Method("total",
								#				self.incometype_total),
							)
		#Reuasable Field
		represent=S3Represent(lookup=tablename, translate=True)
		incometype_id = S3ReusableField("incometype_id", "reference %s" % tablename,
                                               label = T("Income Type"),
											   sortby="name",
											   represent=represent,
                                               requires = IS_EMPTY_OR(IS_ONE_OF(db,
                                                                      "finance_incometype.id", represent)))

		self.configure(tablename,
						listadd=True,
						 )
		self.add_components(tablename,
							finance_incomedetails="incometype_id"
													#{"name" : "details",
													#"joinby" : "incometype_id",
													#"multiple" : True}													}
													)

		
		
						
		return dict(finance_incometype_id=incometype_id)
"""		
def incometype_total(row):
       

	if "finance_incometype" in row:
		incometype_id = row["finance_incometype.id"]
	elif "id" in row:
		incometype_id = row["id"]
	else:
		return 0

	table = current.s3db.finance_incomedetails
	query = (table.deleted != True) & \
			(table.incometype_id == incometype_id)
	sum_field = table.amount.sum()
	return current.db(query).select(sum_field).first()[sum_field] or \
				   current.messages["NONE"]"""
		
#============================================================================================================================
class IncomeDetails(S3Model):

	names = ["finance_incomedetails",
			"finance_incomedetails_id",
			]
	
	def model(self):
		db = current.db
		T = current.T
		settings = current.deployment_settings
	
		
		tablename = "finance_incomedetails"
		table=self.define_table(tablename,
								self.finance_incometype_id(),
								Field("amount", label=T("Amount")),
								Field("person", label=T("Contact Person"))
							)
			
		self.configure(tablename,
						listadd=True,
						)
		
		#Reusable Field
		represent=S3Represent(lookup=tablename, translate=True)
		incomedetails_id = S3ReusableField("incomedetails_id", "reference %s" % tablename,
                                               represent=represent,
                                               requires = IS_EMPTY_OR(IS_ONE_OF(db,
                                                                      "finance_incomedetails.id", represent)))
		
		return dict(finance_incomedetails_id=incomedetails_id)
#============================================================================================================================

class Income(S3Model):
	names = ["finance_income",
			
			]
	
	def model(self):
		db = current.db
		T = current.T
		settings = current.deployment_settings
		
		tablename = "finance_income"
		table = self.define_table(tablename,
									)
		
		self.configure(tablename)
		
		return dict()
	