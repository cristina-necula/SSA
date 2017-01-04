namespace MyProjectManager.Models
{
	public class CurrentUser
	{
		private static readonly CurrentUser instance = new CurrentUser();

		private CurrentUser() { }

		public static CurrentUser Instance
		{
			get
			{
				return instance;
			}
		}

		public User User { get; set; }

	}
}