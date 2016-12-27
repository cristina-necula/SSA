package project_manager

class UserRole {

	String name

    static constraints = {
    	name(
    		blank:false, 
    		nullable:false,
    		size:3..30)
    }

    String toString(){
    	return this.name;
    }
}
