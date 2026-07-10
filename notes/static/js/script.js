const newBtn = document.getElementById("newBtn");
const tableBody = document.getElementById("tableBody");

let counter = 1;

newBtn.addEventListener("click", function () {

    const today = new Date().toLocaleDateString();

    const row = document.createElement("tr");

    row.innerHTML = `
        <td>${counter}</td>

        <td>
            <input type="text" class="name-input" placeholder="Lesson name">
        </td>

        <td>
            <textarea class="note-input" placeholder="Write your note"></textarea>
        </td>

        <td>${today}</td>

        <td>
            <button class="save-btn">Save</button>
        </td>
    `;

    tableBody.appendChild(row);

    const saveBtn = row.querySelector(".save-btn");

    saveBtn.addEventListener("click", function () {

        const lessonName = row.querySelector(".name-input").value;
        const noteText = row.querySelector(".note-input").value;

        row.innerHTML = `
            <td>${counter}</td>
            <td>${lessonName}</td>
            <td>${noteText}</td>
            <td>${today}</td>
            <td>
                <button class="view-btn">View</button>
                <button class="edit-btn">Edit</button>
                <button class="delete-btn">Delete</button>
            </td>
        `;

        const deleteBtn = row.querySelector(".delete-btn");
        const viewBtn = row.querySelector(".view-btn");
        const editBtn = row.querySelector(".edit-btn");

        deleteBtn.addEventListener("click", function () {
            row.remove();
            reorderNumbers();
        });

        viewBtn.addEventListener("click", function () {
            alert(noteText);
        });

        editBtn.addEventListener("click", function () {

            row.innerHTML = `
                <td>${counter}</td>

                <td>
                    <input type="text" class="name-input" value="${lessonName}">
                </td>

                <td>
                    <textarea class="note-input">${noteText}</textarea>
                </td>

                <td>${today}</td>

                <td>
                    <button class="save-btn">Save</button>
                </td>
            `;

        });

        counter++;
    });
});

function reorderNumbers() {
    const rows = tableBody.querySelectorAll("tr");

    rows.forEach((row, index) => {
        row.cells[0].textContent = index + 1;
    });

    counter = rows.length + 1;
}