package project_manager

class Sprint {

	Project project
	String description
	Date startDate
	Date endDate
	Milestone milestone

	static hasMany = [tasks: Task]
	List tasks

	static constraints = {
		description(blank: false)
		milestone(nullable: true)
		tasks(nullable: true)
	}
}