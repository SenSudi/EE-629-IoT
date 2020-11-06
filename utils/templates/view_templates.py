# @login_required(login_url='/login/')
# def model_add_form(request):
# 	form 						= SomeForm()
# 	context['form'] 			= form
# 	context['action'] 			= 'action'
# 	context['form_id'] 			= 'form-model-add'
# 	context['cancel_btn_type'] 	= 'model_name_in_lowers'
# 	context['add_btn_type'] 	= 'model_name_in_lowers'
# 	return render(request,'model_form_modal.html',context)