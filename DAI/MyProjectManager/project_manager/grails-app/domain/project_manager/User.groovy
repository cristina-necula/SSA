package project_manager

class User {

	String username
	String password
	String email
    Date lastLogin
	
	UserRole userRole

    static constraints = {
    	username(
    		blank:false, 
    		nullable:false,
    		size:5..20)
    	password(
    		blank:false,
    		nullable:false,
    		size:5..80)
    	email(
    		blank:false,
    		email:true,
    		nullable:false,
    		size:6..80)
        lastLogin(
            nullable:true,
            display:false)
        userRole(
            nullable:false)
    }

    String toString() {
        return this.username
    }
}
