package com.example;
import jakarta.servlet.*;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.*;
import java.util.ArrayList;
import java.util.List;
@WebServlet("/tasks")
public class TaskManagerServlet extends HttpServlet {
    private static List<Task> tasks = new ArrayList<>();
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        response.setContentType("text/html");
        // Pass tasks to the JSP page
        request.setAttribute("tasks", tasks);
        // Forward to JSP
        RequestDispatcher dispatcher = request.getRequestDispatcher("tasks.jsp");
        dispatcher.forward(request, response);
    }
    //utyttuttyut
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String name = request.getParameter("name");
        String description = request.getParameter("description");
        String dueDate = request.getParameter("dueDate");
        // Create a new task and add it to the list
        Task newTask = new Task(name, description, dueDate);
        tasks.add(newTask);
        System.out.println("Done" + tasks);
        // Redirect to the GET method
        response.sendRedirect("/task-tracker-app/tasks.jsp");
    }
}