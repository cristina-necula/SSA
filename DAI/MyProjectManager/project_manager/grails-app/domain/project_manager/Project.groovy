package project_manager

class Project {
	
	String name
	User projectManager
	
	static hasMany = [members: User]
	List members

	static constraints = {
		name(blank:false)
	}
}