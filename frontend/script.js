
const form = document.getElementById("taskForm");
const input = document.getElementById("taskInput");
const taskList = document.getElementById("taskList");
const message = document.getElementById("message");

const API = "http://127.0.0.1:5000";

async function loadTasks() {
    try {
        const response = await fetch(`${API}/tasks`);
        const tasks = await response.json();

        taskList.replaceChildren();

        tasks.forEach(task => {
            const li = document.createElement("li");
            const name = document.createElement("span");
            name.textContent = task.id + ". " + task.title;

            const del = document.createElement("button");
            del.textContent = "Delete";
            del.className = "delete-btn";
            del.onclick = () => deleteTask(task.id);

            li.append(name, del);
            taskList.appendChild(li);
        });

        message.textContent = "";
    } catch {
        message.textContent = "Backend not running. Please start it.";
    }
}

form.addEventListener("submit", async event => {
    event.preventDefault();

    const title = input.value.trim();
    if (!title) return;

    try {
        const response = await fetch(`${API}/tasks`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title })
        });

        if (!response.ok) throw new Error("Could not add task");

        input.value = "";
        await loadTasks();
    } catch {
        message.textContent = "Could not add task. Check the backend.";
    }
});

async function deleteTask(id) {
    try {
        const response = await fetch(`${API}/tasks/${id}`, {
            method: "DELETE"
        });

        if (!response.ok) throw new Error("Delete failed");
        await loadTasks();
    } catch {
        message.textContent = "Could not delete task.";
    }
}

loadTasks();
