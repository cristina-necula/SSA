using MyProjectManager.Enums;
using System;
using System.Collections.Generic;

namespace MyProjectManager.Helpers
{
	public class RoleToPermissionMapper
	{
		private static readonly Lazy<RoleToPermissionMapper> lazyInstance =
			new Lazy<RoleToPermissionMapper>(() => new RoleToPermissionMapper());

		public static RoleToPermissionMapper Instance
		{
			get
			{
				return lazyInstance.Value;
			}
		}

		public Dictionary<UserRole, List<Permission>> PermissionsDictionary = new Dictionary<UserRole, List<Permission>>();

		private RoleToPermissionMapper()
		{
			PermissionsDictionary.Add(UserRole.AccountsAdministrator,
				new List<Permission> { Permission.CreateUser, Permission.CreateProject });
			PermissionsDictionary.Add(UserRole.ProjectManager,
				new List<Permission> { Permission.CreateProject, Permission.CreateUser, Permission.CreateSprint,
				Permission.CreateTask, Permission.AlocateUser, Permission.EditTask, Permission.EstablishMilestone});
			PermissionsDictionary.Add(UserRole.Developer,
				new List<Permission> { Permission.AlocateUser, Permission.EditTask });
			PermissionsDictionary.Add(UserRole.QualityAssurance,
				new List<Permission> { Permission.AlocateUser, Permission.EditTask });
			PermissionsDictionary.Add(UserRole.Tester,
				new List<Permission> { Permission.AlocateUser, Permission.EditTask });
		}


	}
}