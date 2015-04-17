from s3.s3data import S3DataTable
from s3.s3resource import S3Resource
from s3.s3query import S3FieldSelector


def donations():

	s3db.set_method("finance", "donations", method="total", action=donations_total)
	
	
	return s3_rest_controller()
	
def index():
	return dict()
	
s3.crud_strings["finance_donations"] = Storage(
label_create = T("Create New Donation"),
title_display = T("Donations Details"),
title_list = T("List Donations"),
title_update = T("Edit Donation"),
title_upload = T("Import Donations"),
subtitle_list = T("Donations"),
label_list_button = T("List Donations"),
label_delete_button = T("Delete Donation"),
msg_record_created = T("Donation added"),
msg_record_modified = T("Donation updated"),
msg_record_deleted = T("Donation deleted"),
msg_list_empty = T("No Donations currently registered"))


#Method to calculate total donations

def donations_total(r, **attr):
	table = current.s3db.finance_donations
	tot = table.amount.sum()
	output = current.db().select(tot).first()[tot] or \
			current.messages["NONE"]
	return dict(output=output)
	
#---------------------------------------------------------------------------------------------------------------------------	

def incomedetails():
	
	s3db.set_method("finance", "incomedetails", method="total", action=incomedetails_total)
	
	
	return s3_rest_controller()

s3.crud_strings["finance_incomedetails"] = Storage(
label_create = T("Create New Income Detail"),
title_display = T("Income Details"),
title_list = T("List Income Details"),
title_update = T("Edit Income Details"),
title_upload = T("Import Income Details"),
subtitle_list = T("Donations"),
label_list_button = T("List Income Details"),
label_delete_button = T("Delete Income Detail"),
msg_record_created = T("Income Detail added"),
msg_record_modified = T("Income Detail updated"),
msg_record_deleted = T("Income Detail deleted"),
msg_list_empty = T("No Income Details currently registered"))	
#-----------------------------------------------------------------------------------------------------------------------------

def incometype_rheader(r, tabs=[]):
	if r.representation != "html":
		# RHeader is a UI facility & so skip for other formats
		return None
	if r.record is None:
		# List or Create form: rheader makes no sense here
		return None
	tabs = [(T("Basic Details"), None),
			(T("Income Details"), "incomedetails"),
			(T("Total"),"total"),]
	rheader_tabs = s3_rheader_tabs(r, tabs)
	incometype = r.record
	rheader = DIV(TABLE(
					TR(TH("% s: " % T("Name")), incometype.name,), rheader_tabs))
	return rheader
	


#---------------------------------------------------------------------------------------------------------------------------
def incometype():

	s3db.set_method("finance", "incometype", method="total", action=incometype_total)
	
	return s3_rest_controller(rheader=incometype_rheader)
	
s3.crud_strings["finance_incometype"] = Storage(
label_create = T("Create New Income Type"),
title_display = T("Income Types"),
title_list = T("List Income Types"),
title_update = T("Edit Income Types"),
title_upload = T("Import Income Types"),
subtitle_list = T("Donations"),
label_list_button = T("List Income Types"),
label_delete_button = T("Delete Income Type"),
msg_record_created = T("Income Type added"),
msg_record_modified = T("Income Type updated"),
msg_record_deleted = T("Income Type deleted"),
msg_list_empty = T("No Income Types currently registered"))	
	
#-------------------------------------------------------------------------------------------------------------------------
"""Method to calculate total income if all income types"""
def incomedetails_total(r, **attr):
	
	table = current.s3db.finance_incomedetails
	tot = table.amount.sum()
	output = current.db().select(tot).first()[tot] or \
			current.messages["NONE"]
	return dict(output=output)
	
#--------------------------------------------------------------------------------------------------------------------------
"""Method to calculate total income"""
def totalincome():
	
	table1 = current.s3db.finance_incomedetails
	table2 = current.s3db.finance_donations
	tot1 = table1.amount.sum()
	tot2 = table2.amount.sum()
	output1 = current.db().select(tot1).first()[tot1] or \
			current.messages["NONE"]
	output2 = current.db().select(tot2).first()[tot2] or \
			current.messages["NONE"]
	output = output1 + output2
	return dict(output=output)
#---------------------------------------------------------------------------------------------------------------------------

"""Method to calculate total income of a particular income type"""
def incometype_total(r, **attr):
		
	resource = s3db.resource("finance_incometype")
	table = current.s3db.finance_incometype
	query = (db.finance_incometype.id == r.id) & (db.finance_incomedetails.incometype_id == db.finance_incometype.id)
	component = resource.components["incomedetails"]
	join = component.get_join()
	query&=join
	tot = current.s3db.finance_incomedetails.amount.sum()
	output = current.db(query).select(tot).first()[tot] or \
			current.messages["NONE"]
	return dict(output=output)	
#---------------------------------------------------------------------------------------------------------------------------