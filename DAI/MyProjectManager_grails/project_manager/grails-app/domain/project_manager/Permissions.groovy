package project_manager

class Permissions {

	String name

	static hasMany = [userRoles: UserRole]
	List userRoles

	static constraints = {
		name(blank:false)
	}

}