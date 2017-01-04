using MyProjectManager.DAL;
using MyProjectManager.Models;
using System.Data.Entity;
using System.Linq;
using System.Net;
using System.Web.Mvc;
using MyProjectManager.Helpers;

namespace MyProjectManager.Controllers
{
	public class UsersController : Controller
	{
		private ProjectManagerContext dbContext = new ProjectManagerContext();

		// GET: Users
		public ActionResult Index()
		{
            var model = dbContext.Users.ToList();
			return View(model);
		}

		// GET: Users/Details/5
		public ActionResult Details(int? id)
		{
			if (id == null)
			{
				return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
			}
			User user = dbContext.Users.Find(id);
			if (user == null)
			{
				return HttpNotFound();
			}
			return View(user);
		}

		// GET: Users/Create
		public ActionResult Create()
		{
			return View();
		}

		// POST: Users/Create
		[HttpPost]
		[ValidateAntiForgeryToken]
		public ActionResult Create([Bind(Include = "ID,Username,Email,UserRole")] User user)
		{
			if (ModelState.IsValid)
			{
                User dbUser = dbContext.Users.ToList()
                    .Where(u => u.Email == user.Email || u.Username == user.Username)
                    .FirstOrDefault();

                if(dbUser != null)
                {
                    return FailedAction("User with specified details already exists!", user);
                }

                if (!user.UserRole.HasValue)
                {
                    return FailedAction("Please specify a role for the new user!", user);
                }

				dbContext.Users.Add(user);
				dbContext.SaveChanges();
				return RedirectToAction("Index");
			}

			return View(user);
		}

		// GET: Users/Edit/5
		public ActionResult Edit(int? id)
		{
			if (id == null)
			{
				return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
			}
			User user = dbContext.Users.Find(id);
			if (user == null)
			{
				return HttpNotFound();
			}
			return View(user);
		}

		// POST: Users/Edit/5
		[HttpPost]
		[ValidateAntiForgeryToken]
		public ActionResult Edit([Bind(Include = "ID,Username,FirstName,LastName,Password,Email,UserRole")] User user)
		{
			if (ModelState.IsValid)
			{
				dbContext.Entry(user).State = EntityState.Modified;
				dbContext.SaveChanges();
				return RedirectToAction("Index");
			}
			return View(user);
		}

		// GET: Users/Delete/5
		public ActionResult Delete(int? id)
		{
			if (id == null)
			{
				return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
			}
			User user = dbContext.Users.Find(id);
			if (user == null)
			{
				return HttpNotFound();
			}
			return View(user);
		}

		// POST: Users/Delete/5
		[HttpPost, ActionName("Delete")]
		[ValidateAntiForgeryToken]
		public ActionResult DeleteConfirmed(int id)
		{
			User user = dbContext.Users.Find(id);
			dbContext.Users.Remove(user);
			dbContext.SaveChanges();
			return RedirectToAction("Index");
		}

		protected override void Dispose(bool disposing)
		{
			if (disposing)
			{
				dbContext.Dispose();
			}
			base.Dispose(disposing);
		}

        private ViewResult FailedAction(string message, User user)
        {
            TempData[Constants.NOTICE] = message;
            return View(user);
        }
	}
}
