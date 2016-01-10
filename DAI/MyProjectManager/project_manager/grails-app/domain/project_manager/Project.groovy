package project_manager

class Project {
	
	String name
	User projectManager
	
	//static hasMany = [members: User]

	static constraints = {
		name(blank:false)
		projectManager(blank:false, validator: {value, object -> if (!object.userRole.name.equals("Project Manager")) return false});
	}
}