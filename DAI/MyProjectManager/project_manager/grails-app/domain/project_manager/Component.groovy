package project_manager

class Component {
	String name

	static constraints = {
		name(blank: false)
	}
}