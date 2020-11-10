from methodologies.models import Phase

def get_phase_total_time(phase_id):
	phase = Phase.objects.get(id=phase_id)
	total_time = phase.billed_total_time
	return total_time