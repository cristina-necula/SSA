using MyProjectManager.DAL;
using MyProjectManager.Helpers;
using MyProjectManager.Models;
using System;
using System.Linq;
using System.Web.Mvc;

namespace MyProjectManager.Controllers
{
	public class HomeController : Controller
	{
		private ProjectManagerContext dbContext = new ProjectManagerContext();

		public ActionResult Index()
		{
			return View();
		}

		public ActionResult Login()
		{
			return View();
		}

		public ActionResult Signin()
		{
			return View();
		}

        public ActionResult Activity()
        {
            return View();
        }

		// POST: Users/Login
		[HttpPost]
		[ValidateAntiForgeryToken]
		public ActionResult ValidateLogin([Bind(Include = "Username,Password")] User user)
		{
			if (ModelState.IsValid)
			{
				User dbUser = dbContext.Users.ToList()
                    .Where(u => u.Username.Equals(user.Username) && u.Password.Equals(user.Password))
                    .FirstOrDefault();

				if (dbUser == null)
				{
					TempData[Constants.NOTICE] = "Invalid username or password! Please try again!";
					return RedirectToAction("Login");
				}

				dbUser.LastLogin = DateTime.UtcNow;
				CurrentUser.Instance.User = dbUser;

				dbContext.Entry(dbUser).State = System.Data.Entity.EntityState.Modified;
				dbContext.SaveChanges();

				return RedirectToAction("Activity");
			}
			return RedirectToAction("Login");
		}

		// POST: Users/Signin
		[HttpPost]
		[ValidateAntiForgeryToken]
		public ActionResult ValidateSignin([Bind(Include = "FirstName,LastName,Username,Email,Password")] User user)
		{
			if (ModelState.IsValid)
			{
				User dbUser = dbContext.Users.ToList().Where(u => u.Email.Equals(user.Email)).FirstOrDefault();

				if (dbUser == null)
				{
					return FailedSignIn("Your email address has not been added yet in the system by an account administrator.");
				}

				if (dbUser.UserRole == null)
				{
					return FailedSignIn("Your account administrator has not set an user role for your account yet.");
				}

				if (string.IsNullOrEmpty(user.FirstName) ||
					string.IsNullOrEmpty(user.LastName) ||
					string.IsNullOrEmpty(user.Password) ||
					string.IsNullOrEmpty(user.Username))
				{
                    return FailedSignIn("Please complete all the fields in order to access your account");
				}

				UpdateDbEntry(dbUser, user);

				CurrentUser.Instance.User = dbUser;

                return RedirectToAction("Activity");
            }
			return RedirectToAction("Signin");
		}

		private RedirectToRouteResult FailedSignIn(string message)
		{
			TempData[Constants.NOTICE] = message;
            return RedirectToAction("Signin");
		}

		private void UpdateDbEntry(User userEntry, User userView)
		{
			userEntry.Email = userView.Email;
			userEntry.FirstName = userView.FirstName;
			userEntry.LastName = userView.LastName;
			userEntry.Username = userView.Username;
			userEntry.Password = userView.Password;
			userEntry.LastLogin = DateTime.UtcNow;

			dbContext.Entry(userEntry).State = System.Data.Entity.EntityState.Modified;
			dbContext.SaveChanges();
		}

	}
}