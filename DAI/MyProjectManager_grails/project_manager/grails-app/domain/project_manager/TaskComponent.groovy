package project_manager

class TaskComponent {
	
	int time
	String description

	static constraints = {
		time(blank: false)
		description(blank: false)
	}
}