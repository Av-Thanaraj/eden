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
