using System;
using System.Collections.Generic;
using System.Data;
using System.Data.Entity;
using System.Linq;
using System.Net;
using System.Web;
using System.Web.Mvc;
using MyProjectManager.DAL;
using MyProjectManager.Models;
using System.Web.Routing;
using MyProjectManager.ViewModels;
using MyProjectManager.Helpers;

namespace MyProjectManager.Controllers
{
    public class ProjectsController : Controller
    {
        private ProjectManagerContext db = new ProjectManagerContext();
        static ProjectViewModel projectVM = new ProjectViewModel();

        // GET: Projects
        public ActionResult Index()
        {
            return View(db.Projects.ToList());
        }

        // GET: Projects/Details/5
        public ActionResult Details(int? id)
        {
            if (id == null)
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }
            Project project = db.Projects.Find(id);
            if (project == null)
            {
                return HttpNotFound();
            }
            return View(project);
        }

        // GET: Projects/Create
        public ActionResult Create()
        {
            projectVM = new ProjectViewModel();
            CreateBindings();
            return View(projectVM);
        }

        // POST: Projects/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Create([Bind(Include = "ID,Name,ProjectManagerID,TeamMembers")] ProjectViewModel projectVM)
        {
            if (ModelState.IsValid)
            {
                var project = new Project();

                if (string.IsNullOrWhiteSpace(projectVM.Name))
                {
                    return FailedAction("Please give the project a name in order to save it.", projectVM);
                }
                project.Name = projectVM.Name;

                var projectManager = db.Users.Where(u => u.ID == projectVM.ProjectManagerID).FirstOrDefault();
                if(projectManager == null)
                {
                    return FailedAction("Selected project manager was not found.", projectVM);
                }
                project.ProjectManager = projectManager;

                if(projectVM.TeamMembers.Count > 0)
                {
                    project.TeamMembers = new List<User>();
                }

                foreach(var user in projectVM.TeamMembers)
                {
                    var userDb = db.Users.Where(u => u.Username == user.Username).FirstOrDefault();

                    if (userDb == null)
                    {
                        return FailedAction("User with username " + user.Username + " was not found.", projectVM);
                    }
                    if(userDb.UserRole == Enums.UserRole.ProjectManager || userDb.UserRole == Enums.UserRole.AccountsAdministrator)
                    {
                        return FailedAction("Cannot add user with role " + userDb.UserRole.ToString() + " as a team member", projectVM);
                    }

                    project.TeamMembers.Add(userDb);
                }

                db.Projects.Add(project);
                db.SaveChanges();
                return RedirectToAction("Index");
            }

            projectVM = new ProjectViewModel();
            return View(projectVM);
        }

        // GET: Projects/Edit/5
        public ActionResult Edit(int? id)
        {
            if (id == null)
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }
            Project project = db.Projects.Find(id);
            if (project == null)
            {
                return HttpNotFound();
            }
            return View(project);
        }

        // POST: Projects/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Edit([Bind(Include = "ID,Name")] Project project)
        {
            if (ModelState.IsValid)
            {
                db.Entry(project).State = EntityState.Modified;
                db.SaveChanges();
                return RedirectToAction("Index");
            }
            return View(project);
        }

        // GET: Projects/Delete/5
        public ActionResult Delete(int? id)
        {
            if (id == null)
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }
            Project project = db.Projects.Find(id);
            if (project == null)
            {
                return HttpNotFound();
            }
            return View(project);
        }

        // POST: Projects/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public ActionResult DeleteConfirmed(int id)
        {
            Project project = db.Projects.Find(id);
            db.Projects.Remove(project);
            db.SaveChanges();
            return RedirectToAction("Index");
        }

        public ActionResult CreateBindings()
        {
            var projectManagers = db.Users.Where(u => u.UserRole == Enums.UserRole.ProjectManager);
            ViewBag.ProjectManagers = new SelectList(projectManagers, "Id", "Username");
           
            return View();
        }

        public ActionResult AddNewProjectMember()
        {
            return PartialView("~/Views/EditorTemplates/ProjectTeamMemberEditor.cshtml", new User());
        }

        protected override void Dispose(bool disposing)
        {
            if (disposing)
            {
                db.Dispose();
            }
            base.Dispose(disposing);
        }

        private ViewResult FailedAction(string message, ProjectViewModel projectVM)
        {
            projectVM.TeamMembers = new List<User>();
            CreateBindings();
            TempData[Constants.NOTICE] = message;
            return View(projectVM);
        }
    }
}
