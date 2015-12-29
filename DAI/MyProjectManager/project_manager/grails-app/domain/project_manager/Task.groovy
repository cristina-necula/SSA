package project_manager

class Task {

	Status status
	User responsible
	Component component
	String summary
	int estimaedEffort
	int consumedEffort

	static hasMany = [taskComponents: TaskComponent]
	List taskComponents

	static constraints = {
		responsible(nullable: true)
		summary(blank: false)
		consumedEffort(nullable: true, editable:false)
	}
}