package project_manager

class Milestone {
	String description
	Date estimatedDate
	Date finishDate

	static constraints = {
		description(blank: false)
	}
}