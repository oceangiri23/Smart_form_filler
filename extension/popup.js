let extractedData = null;
const status = document.getElementById("status");
const fillButton = document.getElementById("fillFormsButton");
const uploadArea = document.getElementById("uploadArea");
const imageInput = document.getElementById("imageInput");

document.getElementById("uploadButton").addEventListener("click", async () => {
  const fileInput = document.getElementById("fileInput");
  if (fileInput.files.length === 0) {
    alert("Please upload an image.");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    const response = await fetch("http://localhost:8000/process-document", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error("Failed to process document");

    const data = await response.json();
    chrome.storage.local.set({ extractedData: data }, () => {
      alert("Data extracted! Click 'Fill Forms' to autofill.");
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        console.log(tabs);
        chrome.tabs.sendMessage(tabs[0].id, { action: "updatePage" });
      });
    });
  } catch (error) {
    alert("Error processing document.");
    console.error(error);
  }
});

// function showStep(stepNumber) {
//   // Update steps indicator
//   document.querySelectorAll(".step").forEach((step, index) => {
//     if (index + 1 < stepNumber) {
//       step.classList.add("complete");
//       step.classList.remove("active");
//     } else if (index + 1 === stepNumber) {
//       step.classList.add("active");
//       step.classList.remove("complete");
//     } else {
//       step.classList.remove("active", "complete");
//     }
//   });

//   // Show correct step content
//   document.querySelectorAll(".step-content").forEach((content) => {
//     content.classList.remove("active");
//     if (content.dataset.step === stepNumber.toString()) {
//       content.classList.add("active");
//     }
//   });
// }

// uploadArea.addEventListener("click", () => {
//   imageInput.click();
// });

// imageInput.addEventListener("change", async (e) => {
//   if (e.target.files && e.target.files[0]) {
//     const file = e.target.files[0];
//     showStep(2);
//     status.innerHTML = `
//       <div style="display: flex; align-items: center; justify-content: center; gap: 8px;">
//         <div class="w-5 h-5 border-2 border-primary border-t-transparent rounded-full animate-spin"></div>
//         Processing document...
//       </div>
//     `;

//     try {
//       extractedData = await FormFillerService.processImage(file);
//       showStep(3);
//     } catch (error) {
//       status.innerHTML = `
//         <div style="color: #ef4444;">
//           Error: ${error.message}
//         </div>
//       `;
//       setTimeout(() => showStep(1), 3000);
//     }
//   }
// });

fillButton.addEventListener("click", async () => {
  if (!extractedData) return;

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: fillFormsWithData,
    args: [extractedData],
  });
});

document
  .getElementById("fillFormsButton")
  .addEventListener("click", async () => {
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });

    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: () => {
        // Get all input fields that have our wrapper (meaning they're fillable)
        const fillableInputs = document.querySelectorAll(
          ".form-fill-wrapper input, .form-fill-wrapper select"
        );

        fillableInputs.forEach((input) => {
          // Find the associated fill icon and trigger its click event
          const fillIcon = input.parentElement.querySelector(".form-fill-icon");
          if (fillIcon) {
            fillIcon.click();
          }
        });
      },
    });
  });

// function fillFormsWithDummyData() {
//   // This function will be injected into the page
//   const event = new Event("change", { bubbles: true });

//   // Trigger the form fill
//   document.dispatchEvent(new CustomEvent("fillFormsButton"));
// }

// function fillFormsWithData(data) {
//   // This function will be injected into the page
//   document.dispatchEvent(new CustomEvent("fillFormsButton", { detail: data }));
// }
