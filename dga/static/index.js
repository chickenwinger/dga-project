const recordModal = document.getElementById("recordModal");
recordModal.addEventListener("show.bs.modal", (event) => {
  // Button that triggered the modal
  const button = event.relatedTarget;
  // Extract info from data-bs-* attributes
  const type = button.getAttribute("data-bs-type");
  // If necessary, you could initiate an Ajax request here
  // and then do the updating in a callback.
  //
  // Update the modal's content.
  const modalTitle = recordModal.querySelector(".modal-title");
  const modalBodyInput = recordModal.querySelector(".modal-body input");

  modalTitle.textContent = `Add new record of ${type.toUpperCase()}`;
});

function formatGaseousContent(gaseousContent) {
  const transformedContent = transformGaseousContent(gaseousContent);
  let formattedContent = '';

  for (const key in transformedContent) {
    if (transformedContent.hasOwnProperty(key)) {
      formattedContent += `${key}: ${transformedContent[key]}<br>`;
    }
  }

  return formattedContent;
}

function transformGaseousContent(gaseousContent) {
  const result = {};

  for (const key in gaseousContent) {
    if (gaseousContent.hasOwnProperty(key) && key !== 'timestamp') {
      result[`${key}`] = gaseousContent[key];
    }
  }

  return result;
}

function loadData() {
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/get_table_data", true);
  xhr.responseType = "json";
  xhr.onload = function () {
    if (xhr.status === 200) {
      updateTable(xhr.response);
    } else {
      console.error("Error fetching data:", xhr.statusText);
    }
  };
  xhr.send();
}

function updateTable(data) {
  const tableBody = document.querySelector("#data-table tbody");
  tableBody.innerHTML = "";

  // Fetch the URL from the hidden element's data attribute
  const recordsUrl = document.querySelector("#url-container").dataset.url;
  
  if (data.length === 0) {
    const noDataRow = `
    <tr>
      <td colspan="3">No data</td>
    </tr>
  `;
  tableBody.insertAdjacentHTML("beforeend", noDataRow);
  } else {
    data.forEach((row) => {
      const tagNum = row.tag_num;
      const gaseousContent = formatGaseousContent(row.gaseous_content);
      const faultValue = row.fault;

      const tableRow = `
        <tr class="position-relative">
          <th scope="row"><a href="${recordsUrl}" class="stretched-link">${tagNum}</a></th>
          <td>${gaseousContent}</td>
          <td>${faultValue}</td>
        </tr>
      `;

      tableBody.insertAdjacentHTML("beforeend", tableRow);
    });
  }
}

document.addEventListener("DOMContentLoaded", function () {
  loadData();
});
