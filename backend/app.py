
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Create logs folder and configure logging
log_dir = Path(__file__).resolve().parent / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    filename=str(log_dir / "app.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# Home route
@app.route("/")
def home():
    app.logger.info("Home endpoint accessed")
    return "Task Manager Backend is running!"


# Temporary in-memory storage
tasks = []
next_id = 1


# Get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    app.logger.info("Fetching all tasks; count=%d", len(tasks))
    return jsonify(tasks)


# Add a task
@app.route("/tasks", methods=["POST"])
def add_task():
    global next_id

    data = request.get_json(silent=True) or {}
    title = data.get("title", "")

    if not isinstance(title, str) or not title.strip():
        app.logger.warning("Task creation rejected: title missing or invalid")
        return jsonify({"error": "Task title is required"}), 400

    title = title.strip()
    task = {"id": next_id, "title": title}
    tasks.append(task)
    next_id += 1

    app.logger.info("Task created; task_id=%d", task["id"])
    return jsonify(task), 201


# Delete a task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            app.logger.info("Task deleted; task_id=%d", task_id)
            return jsonify({"message": "Task deleted"})

    app.logger.warning("Task deletion failed: task_id=%d not found", task_id)
    return jsonify({"error": "Task not found"}), 404


if __name__ == "__main__":
    app.logger.info("Task Manager backend starting")
    app.run(host="0.0.0.0", port=5000, debug=False)
