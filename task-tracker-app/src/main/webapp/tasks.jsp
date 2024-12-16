<%@ page import="java.util.List" %>
<%@ page import="com.example.Task" %>
<!DOCTYPE html>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Manager</title>
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Task Manager</h1>

    <!-- Task Form -->
    <form action="/task-tracker-app/tasks" method="POST">
        <h2>Add Task</h2>
        Task Name: <input type="text" name="name" required><br>
        Description: <input type="text" name="description" required><br>
        Due Date: <input type="date" name="dueDate" required><br>
        <input type="submit" value="Add Task">
    </form>

    <!-- Task Table -->
    <h2>Task List</h2>
    <table>
        <tr>
            <th>Check</th>
            <th>Task Name</th>
            <th>Description</th>
            <th>Due Date</th>
        </tr>
        <% 
            List<Task> tasks = (List<Task>) request.getAttribute("tasks");
            if (tasks != null && !tasks.isEmpty()) {
                for (Task task : tasks) {
        %>
        <tr>
            <td><input type="checkbox"></td>
            <td><%= task.getName() %></td>
            <td><%= task.getDescription() %></td>
            <td><%= task.getDueDate() %></td>
        </tr>
        <% 
                }
            } else {
        %>
        <tr>
            <td colspan="4">No tasks added yet.</td>
        </tr>
        <% } %>
    </table>
</body>
</html>
