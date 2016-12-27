package project_manager

class LoginController {

    def index() { }

    def login = {
    	
    	def user = User.findWhere(username:params['username'], password:params['password'])
		session.user = user
    	
    	if(user){
    		user.lastLogin = new Date()
    		flash.message = "Login Successful"
    		redirect(action: 'index')
    	}
    	else {
    		flash.message = "Login Failed"
    		redirect(action: 'index')
    	}
    }
}
