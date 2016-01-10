<html>
	<head>
		<title>Login</title>
		<style type="text/css">
			label{
				float: left;
				width: 65px;
			}
		</style>	
	</head>
	<body>
		${flash.message}
		<g:form action="login" style="padding-left:200px">
			<div>
				<label>Username:</label>
				<input type="text" name="username"/>
				<br/>
				<label>Password:</label>
				<input type="password" name="password"/>
				<br/>
				<input style="width:200px" type="submit" value="Login">
			</div>
		</g:form>
	</body>
</html>
